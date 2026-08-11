"""
Advisory Service for AgriAI Advisor
Combines disease predictions with live weather and 24h/7d forecasts
to run a transparent climate-risk engine and generate actionable guidance.
"""

DISEASE_GUIDANCE_DATABASE = {
    "Tomato Late Blight": {
        "whats_wrong": "Your tomato leaf shows signs consistent with Late Blight (Phytophthora infestans), a fast-spreading fungal-like pathogen.",
        "what_to_do": "Promptly remove and safely destroy heavily infected leaves and stems. Apply registered protective copper or bio-fungicide sprays following local extension guidelines.",
        "prevention": "Ensure wide plant spacing for optimum canopy ventilation. Stake vines off soil and use drip irrigation instead of overhead sprinklers.",
        "humidity_threshold": 75,
        "moisture_sensitive": True
    },
    "Tomato Early Blight": {
        "whats_wrong": "Your tomato leaf exhibits target-ring concentric brown lesions typical of Early Blight (Alternaria solani).",
        "what_to_do": "Prune lower leaves touching wet soil. Apply approved protective foliar fungicides or bio-agents when disease symptoms first appear.",
        "prevention": "Rotate crops with non-solanaceous plants every 2-3 years. Mulch soil around plant bases to reduce splash dispersal of fungal spores.",
        "humidity_threshold": 70,
        "moisture_sensitive": True
    },
    "Tomato Bacterial Spot": {
        "whats_wrong": "Your tomato plant shows symptoms consistent with Bacterial Spot (Xanthomonas spp.), causing dark greasy leaf spots.",
        "what_to_do": "Avoid field operations while foliage is wet. Apply copper-based bactericides combined with mancozeb where recommended by local experts.",
        "prevention": "Use certified disease-free seeds and seedlings. Sanitize farming equipment and destroy infected crop residue after harvest.",
        "humidity_threshold": 70,
        "moisture_sensitive": True
    },
    "Tomato Healthy": {
        "whats_wrong": "Your tomato crop leaves appear healthy with no evident disease symptoms.",
        "what_to_do": "Continue routine crop monitoring and maintain balanced plant nutrition and regular watering.",
        "prevention": "Keep weed density low around crop rows and inspect foliage weekly for early signs of pests or disease.",
        "humidity_threshold": 90,
        "moisture_sensitive": False
    },
    "Potato Late Blight": {
        "whats_wrong": "Your potato foliage shows symptoms of Late Blight, which can cause rapid leaf decay and tuber rot in wet conditions.",
        "what_to_do": "Inspect nearby plants immediately. Apply recommended protective fungicides to healthy foliage before rain events.",
        "prevention": "Hill soil properly around potato stems to protect tubers from spores washed down by rain. Plant resistant cultivars.",
        "humidity_threshold": 75,
        "moisture_sensitive": True
    },
    "Potato Early Blight": {
        "whats_wrong": "Your potato leaf exhibits dark brown concentric spots indicating Early Blight infection.",
        "what_to_do": "Remove affected lower leaves. Ensure adequate nitrogen and potassium fertilization to support plant vigor.",
        "prevention": "Maintain consistent soil moisture and eliminate solanaceous weeds near the field borders.",
        "humidity_threshold": 70,
        "moisture_sensitive": True
    },
    "Potato Healthy": {
        "whats_wrong": "Your potato plant leaves appear healthy and robust.",
        "what_to_do": "Maintain standard agronomic field practices and monitor moisture levels.",
        "prevention": "Practice 3-year crop rotation and inspect fields after major rain showers.",
        "humidity_threshold": 90,
        "moisture_sensitive": False
    },
    "Corn Common Rust": {
        "whats_wrong": "Your corn leaf shows reddish-brown powdery pustules indicative of Common Rust (Puccinia sorghi).",
        "what_to_do": "In most cases, rust on mature corn requires no chemical intervention. For severe early infections, consult local extension for resistant varieties.",
        "prevention": "Plant rust-resistant corn hybrids suited for your climatic zone.",
        "humidity_threshold": 80,
        "moisture_sensitive": True
    },
    "Corn Healthy": {
        "whats_wrong": "Your corn foliage is healthy with excellent chlorophyll development.",
        "what_to_do": "Maintain proper nitrogen sidedressing and weed management.",
        "prevention": "Ensure adequate field drainage during heavy seasonal monsoon rain.",
        "humidity_threshold": 90,
        "moisture_sensitive": False
    },
    "Pepper Bacterial Spot": {
        "whats_wrong": "Your pepper foliage displays leaf spot lesions consistent with Bacterial Spot.",
        "what_to_do": "Remove severely infected foliage. Apply approved copper bactericides strictly following label directions.",
        "prevention": "Avoid handling plants when wet. Use drip irrigation and maintain crop rotation.",
        "humidity_threshold": 70,
        "moisture_sensitive": True
    },
    "Pepper Healthy": {
        "whats_wrong": "Your pepper crop leaves are healthy and clean.",
        "what_to_do": "Maintain optimal irrigation schedule and inspect lower leaves periodically.",
        "prevention": "Mulch beds to reduce soil splash onto lower foliage.",
        "humidity_threshold": 90,
        "moisture_sensitive": False
    }
}

# Generic fallback guidance
GENERIC_GUIDANCE = {
    "whats_wrong": "Foliage shows signs of localized stress or infection.",
    "what_to_do": "Inspect nearby crop leaves carefully. Prune affected leaves and consult your local agricultural extension service.",
    "prevention": "Ensure good soil drainage, adequate plant spacing, and clean crop sanitation.",
    "humidity_threshold": 75,
    "moisture_sensitive": True
}


def generate_advisory(disease_info, weather_info):
    """
    Combines disease analysis and Open-Meteo weather data to generate:
    1. Climate-Disease Risk Level (LOW, MEDIUM, HIGH)
    2. Weather-based Risk Assessment text
    3. Actionable Farmer Advisory Sections
    4. "Best Time to Act" weather window recommendation
    """
    display_title = disease_info.get("display_title", "Crop Disease")
    disease_name = disease_info.get("disease_name", "Condition")
    crop = disease_info.get("crop", "Crop")
    
    # Retrieve disease database entry or generic fallback
    guidance = DISEASE_GUIDANCE_DATABASE.get(display_title, GENERIC_GUIDANCE)
    if guidance == GENERIC_GUIDANCE and disease_name == "Healthy":
        guidance = {
            "whats_wrong": f"Your {crop} foliage appears healthy with no visible pathogen infection.",
            "what_to_do": "Continue routine field monitoring and maintain balanced irrigation and crop nutrition.",
            "prevention": "Keep field borders clean of weeds and monitor leaf surfaces twice weekly.",
            "humidity_threshold": 90,
            "moisture_sensitive": False
        }
    
    # Extract weather metrics
    current_weather = weather_info.get("current", {})
    temp = current_weather.get("temperature", 28.0)
    humidity = current_weather.get("humidity", 70)
    rain_prob = current_weather.get("rain_probability", 30)
    precipitation = current_weather.get("precipitation", 0.0)
    wind_speed = current_weather.get("wind_speed", 10.0)
    condition = current_weather.get("condition", "Clear")
    
    forecast_24h = weather_info.get("forecast_24h", [])
    
    # Check if rain is expected in next 12-24h
    rain_in_12h = any(h.get("rain_prob", 0) >= 50 for h in forecast_24h[:12])
    high_rain_prob_24h = any(h.get("rain_prob", 0) >= 60 for h in forecast_24h[:24])
    
    # -------------------------------------------------------------
    # 1. WEATHER-BASED RISK ENGINE
    # -------------------------------------------------------------
    is_healthy = "healthy" in disease_name.lower() or disease_info.get("severity") == "NONE"
    
    if is_healthy:
        if humidity > 85 and (rain_prob > 60 or precipitation > 2.0):
            risk_level = "MEDIUM"
            risk_badge = "risk-medium"
            weather_risk_assessment = (
                f"While foliage is currently healthy, high ambient humidity ({humidity}%) "
                f"and expected rainfall ({rain_prob}% probability) elevate the environmental risk of fungal spore germination."
            )
        else:
            risk_level = "LOW"
            risk_badge = "risk-low"
            weather_risk_assessment = (
                f"Favorable weather conditions (Temperature: {temp}°C, Humidity: {humidity}%). "
                f"Low climate risk for disease outbreak at present."
            )
    else:
        # Diseased crop risk calculation
        moisture_risk = (humidity >= guidance["humidity_threshold"]) or (rain_prob >= 50) or (precipitation > 0.5)
        high_moisture_risk = (humidity >= 80 and rain_prob >= 60) or (precipitation >= 3.0) or high_rain_prob_24h
        
        if high_moisture_risk or guidance["moisture_sensitive"] and moisture_risk:
            risk_level = "HIGH"
            risk_badge = "risk-high"
            weather_risk_assessment = (
                f"CRITICAL RISK: High humidity ({humidity}%) and forecasted rain ({rain_prob}% probability) "
                f"create ideal conditions for rapid spread of {disease_name}. Spores germinate rapidly on wet leaves."
            )
        elif moisture_risk or humidity >= 65:
            risk_level = "MEDIUM"
            risk_badge = "risk-medium"
            weather_risk_assessment = (
                f"MODERATE RISK: Current humidity ({humidity}%) and temperature ({temp}°C) "
                f"may favor gradual disease development. Monitor weather updates closely."
            )
        else:
            risk_level = "LOW"
            risk_badge = "risk-low"
            weather_risk_assessment = (
                f"LOW RISK: Dry weather ({humidity}% humidity, low rain probability) "
                f"slows down active pathogen replication."
            )

    # -------------------------------------------------------------
    # 2. WEATHER WARNING
    # -------------------------------------------------------------
    if rain_prob > 60 or precipitation > 1.0:
        weather_warning = f"High humidity ({humidity}%) and expected rainfall ({rain_prob}% chance) may increase disease spread."
    elif humidity > 80:
        weather_warning = f"High humidity level ({humidity}%) keeps crop leaves wet, encouraging fungal spore growth."
    elif wind_speed > 22.0:
        weather_warning = f"High wind speeds ({wind_speed} km/h) may spread spores to neighboring fields."
    else:
        weather_warning = f"Weather is currently stable ({temp}°C, {humidity}% humidity). Maintain standard vigilance."

    # -------------------------------------------------------------
    # 3. BEST TIME TO ACT FEATURE
    # -------------------------------------------------------------
    if is_healthy:
        best_time_to_act = {
            "title": "Routine Maintenance Window",
            "recommendation": "Conditions are favorable for regular field scouting. Recheck weather before any scheduled irrigation.",
            "status_icon": "✅",
            "badge_color": "green"
        }
    elif wind_speed > 25.0:
        best_time_to_act = {
            "title": "High Wind Warning - Delay Spraying",
            "recommendation": f"Wind speed is currently {wind_speed} km/h. Avoid applying foliar treatments to prevent spray drift. Wait for wind speeds to drop below 15 km/h.",
            "status_icon": "💨",
            "badge_color": "amber"
        }
    elif rain_in_12h or rain_prob >= 65:
        best_time_to_act = {
            "title": "Act Before Expected Rain",
            "recommendation": f"Rain expected within the next 12-24 hours ({rain_prob}% chance). Consider taking preventive field action or removing infected leaves before rainfall, and avoid applying foliar sprays immediately before heavy rain.",
            "status_icon": "⏰",
            "badge_color": "amber"
        }
    elif rain_prob < 30 and humidity < 75:
        best_time_to_act = {
            "title": "Optimal Field Action Window",
            "recommendation": "Dry conditions expected in the upcoming forecast. This provides a clear, effective window for field inspection, sanitation, and treatment subject to product label guidance.",
            "status_icon": "☀️",
            "badge_color": "green"
        }
    else:
        best_time_to_act = {
            "title": "Monitor Local Forecast",
            "recommendation": "Forecast conditions are moderately variable. Recheck local weather updates before carrying out weather-sensitive field applications.",
            "status_icon": "🌤️",
            "badge_color": "blue"
        }

    # -------------------------------------------------------------
    # 4. DISCLOSURE & PESTICIDE NOTICE
    # -------------------------------------------------------------
    pesticide_notice = "Follow the product label and local agricultural extension guidance."

    return {
        "risk_level": risk_level,
        "risk_badge": risk_badge,
        "weather_risk_assessment": weather_risk_assessment,
        "whats_wrong": guidance["whats_wrong"],
        "what_should_i_do": guidance["what_to_do"],
        "prevention": guidance["prevention"],
        "weather_warning": weather_warning,
        "best_time_to_act": best_time_to_act,
        "pesticide_notice": pesticide_notice
    }
