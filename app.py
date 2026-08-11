import os
import uuid
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from services.disease_detection import predict_disease
from services.weather_service import geocode_location, get_weather_and_forecast, get_fallback_weather
from services.advisory_service import generate_advisory

app = Flask(__name__)

# Security & Upload configuration
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB limit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serves the main AgriAI Advisor single-page landing and analysis app."""
    return render_template('index.html')


@app.route('/result')
def result_page():
    """Alternative result view page for standard navigation."""
    return render_template('result.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Main Analysis Endpoint.
    Processes uploaded crop leaf photo, selected crop, and location string or coordinates.
    Returns complete AI disease detection, weather data, risk level, and agronomic advisory.
    """
    is_demo = request.form.get('is_demo', 'false').lower() == 'true'
    crop = request.form.get('crop', 'Tomato').strip()
    location_input = request.form.get('location', '').strip()
    lat_str = request.form.get('lat', '')
    lon_str = request.form.get('lon', '')

    # 1. Image upload handling
    image_url = None
    saved_filepath = None

    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        if not allowed_file(file.filename):
            return jsonify({
                "status": "error",
                "message": "Please upload JPG, JPEG, PNG, or WEBP."
            }), 400
        
        filename = secure_filename(file.filename)
        unique_id = uuid.uuid4().hex[:8]
        filename = f"{unique_id}_{filename}"
        saved_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(saved_filepath)
        image_url = f"/static/uploads/{filename}"
    elif not is_demo:
        return jsonify({
            "status": "error",
            "message": "Please upload a crop leaf image."
        }), 400

    # Handle Demo Mode if requested or fallback
    if is_demo or not saved_filepath:
        image_url = "/static/uploads/demo_sample_leaf.jpg"
        if not location_input:
            location_input = "Vijayawada"
        
        disease_res = _get_demo_disease(crop)
    else:
        # 2. Real AI Disease Detection
        disease_res = predict_disease(saved_filepath, selected_crop=crop)

    # 3. Weather Retrieval & Geocoding
    if lat_str and lon_str:
        try:
            lat = float(lat_str)
            lon = float(lon_str)
            loc_meta = {
                "name": location_input if location_input else "Current Location",
                "lat": lat,
                "lon": lon
            }
        except ValueError:
            loc_meta = geocode_location(location_input if location_input else "Vijayawada")
    else:
        if not location_input:
            location_input = "Vijayawada"
        loc_meta = geocode_location(location_input)

    weather_res = get_weather_and_forecast(
        lat=loc_meta["lat"],
        lon=loc_meta["lon"],
        location_name=loc_meta["name"]
    )

    # 4. Actionable Advisory & Climate Risk Engine
    advisory_res = generate_advisory(disease_res, weather_res)

    # 5. Formulate final response object
    response_payload = {
        "status": "success",
        "is_demo": is_demo,
        "demo_label": "Demo Data" if is_demo else "",
        "crop": crop,
        "image_url": image_url,
        "disease": {
            "title": disease_res.get("display_title", f"{crop} Disease"),
            "raw_class": disease_res.get("raw_class", "Tomato___Late_blight"),
            "disease_name": disease_res.get("disease_name", "Late Blight"),
            "crop_type": disease_res.get("crop", crop),
            "confidence": disease_res.get("confidence", 92.0),
            "severity": disease_res.get("severity", "HIGH"),
            "is_low_confidence": disease_res.get("is_low_confidence", False),
            "confidence_message": disease_res.get("confidence_message", ""),
            "model_status": disease_res.get("model_status", "active"),
            "description": disease_res.get("description", "")
        },
        "weather": {
            "location_name": weather_res["location_name"],
            "lat": weather_res["lat"],
            "lon": weather_res["lon"],
            "current": weather_res["current"],
            "forecast_24h": weather_res["forecast_24h"],
            "forecast_7day": weather_res["forecast_7day"],
            "status": weather_res.get("status", "success")
        },
        "advisory": advisory_res
    }

    return jsonify(response_payload)


@app.route('/api/demo-samples', methods=['GET'])
def get_demo_samples():
    """Returns preset demo sample cards for hackathon quick testing."""
    samples = [
        {
            "id": "demo1",
            "crop": "Tomato",
            "location": "Vijayawada",
            "disease": "Tomato Late Blight",
            "confidence": 94.2,
            "weather": "High Rain Risk (84% Humidity)",
            "image": "https://images.unsplash.com/photo-1592417817098-8f3d6eb1b7a5?w=500&auto=format&fit=crop&q=60"
        },
        {
            "id": "demo2",
            "crop": "Potato",
            "location": "Anand",
            "disease": "Potato Early Blight",
            "confidence": 88.7,
            "weather": "Moderate Humidity (72%)",
            "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=500&auto=format&fit=crop&q=60"
        },
        {
            "id": "demo3",
            "crop": "Corn",
            "location": "Ludhiana",
            "disease": "Corn Common Rust",
            "confidence": 91.5,
            "weather": "Sunny & Clear (45% Humidity)",
            "image": "https://images.unsplash.com/photo-1601593346740-925612772716?w=500&auto=format&fit=crop&q=60"
        }
    ]
    return jsonify({"status": "success", "samples": samples})


def _get_demo_disease(crop):
    """Helper to return realistic disease objects in demo mode."""
    crop_lower = crop.lower()
    if "potato" in crop_lower:
        return {
            "display_title": "Potato Early Blight",
            "raw_class": "Potato___Early_blight",
            "disease_name": "Early Blight",
            "crop": "Potato",
            "confidence": 89.4,
            "severity": "MEDIUM",
            "description": "Dark brown spots with concentric target rings on lower foliage.",
            "is_low_confidence": False,
            "confidence_message": "",
            "model_status": "demo"
        }
    elif "corn" in crop_lower:
        return {
            "display_title": "Corn Common Rust",
            "raw_class": "Corn_(maize)___Common_rust_",
            "disease_name": "Common Rust",
            "crop": "Corn",
            "confidence": 91.2,
            "severity": "MEDIUM",
            "description": "Reddish-brown powdery pustules on upper leaf surface.",
            "is_low_confidence": False,
            "confidence_message": "",
            "model_status": "demo"
        }
    elif "pepper" in crop_lower:
        return {
            "display_title": "Pepper Bacterial Spot",
            "raw_class": "Pepper,_bell___Bacterial_spot",
            "disease_name": "Bacterial Spot",
            "crop": "Pepper",
            "confidence": 87.6,
            "severity": "HIGH",
            "description": "Small dark water-soaked spots causing premature leaf drop.",
            "is_low_confidence": False,
            "confidence_message": "",
            "model_status": "demo"
        }
    else:
        return {
            "display_title": "Tomato Late Blight",
            "raw_class": "Tomato___Late_blight",
            "disease_name": "Late Blight",
            "crop": "Tomato",
            "confidence": 93.8,
            "severity": "HIGH",
            "description": "Large pale brown lesions with white mold under leaf surface in high humidity.",
            "is_low_confidence": False,
            "confidence_message": "",
            "model_status": "demo"
        }


# Error Handlers
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        "status": "error",
        "message": "File size exceeds 10MB limit. Please upload a smaller image."
    }), 413


@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404


if __name__ == '__main__':
    print("AgriAI Advisor Flask Backend Starting on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
