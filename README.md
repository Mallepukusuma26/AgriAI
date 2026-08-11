# 🌾 AgriAI Advisor: Climate-Resilient Agricultural Decision Support

**“From Field Conditions to Smart Farming Decisions.”**

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-brightgreen.svg)](https://www.python.org/)
[![Flask 3.1](https://img.shields.io/badge/Flask-3.1.3-blue.svg)](https://flask.palletsprojects.com/)
[![TensorFlow 2.15+](https://img.shields.io/badge/TensorFlow-2.15%2B-orange.svg)](https://www.tensorflow.org/)
[![Open-Meteo API](https://img.shields.io/badge/Weather-Open--Meteo-0284c7.svg)](https://open-meteo.com/)

---

## 📌 Problem Statement & Solution

### The Challenge
Smallholder farmers face increasing crop losses due to rapidly mutating leaf pathogens coupled with erratic climate patterns. Farmers often lack direct access to expert agronomists in real-time and struggle to make weather-sensitive field decisions (such as when to spray or prune) before heavy monsoon rains wash away treatments or accelerate fungal spore germination.

### The Solution
**AgriAI Advisor** acts as a real-time intelligent bridge between raw unstructured field inputs (**Diseased Leaf Image + Farmer Location + Live Weather**) and expert agronomic guidance. Using deep learning transfer models (**MobileNetV2**) combined with live **Open-Meteo** microclimate data, AgriAI Advisor calculates overall climate-disease risk levels (LOW, MEDIUM, HIGH) and provides farmers with actionable, non-jargon advice including an explicit **⏰ Best Time to Act** forecast window.

---

## 🚀 Key Features

1. **Smart AI Leaf Disease Diagnosis**: Preprocessing (224x224 RGB normalization) and MobileNetV2 classification supporting Tomato, Potato, Corn, Pepper, Apple, and Grape diseases with confidence scoring and low-confidence warnings (<60%).
2. **Hyper-Local Climate Sync**: Automated location geocoding and live Open-Meteo Weather API querying for temperature, relative humidity, wind speed, rain probability, and 24-hour forecast.
3. **Climate / Disease Risk Engine**: Rule-based agronomic risk matrix calculating interaction between pathogen moisture vulnerability and upcoming precipitation.
4. **Actionable Farmer Advisory**:
   - **What's Wrong?**: Simple diagnostic explanation.
   - **What Should I Do?**: Practical treatment and sanitation advice.
   - **Prevention**: Long-term agricultural prevention.
   - **Weather Warning**: Impact of humidity and rainfall on spore germination.
5. **⏰ "Best Time to Act" Feature**: Analyzes upcoming 12-24h weather windows to recommend safer field action timing (e.g. action before rain, dry period execution, or wind-drift delay).
6. **Farmer-Friendly Design & Multi-Language**: Responsive mobile-first UI with nature-inspired green palette, drag-and-drop file upload, GPS location auto-detect, and English / Telugu (తెలుగు) / Hindi (हिन्दी) language toggle.
7. **Offline Hackathon Demo Mode**: Built-in toggle supporting offline sample datasets for Vijayawada, Anand, and Ludhiana.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | HTML5, CSS3 (Vanilla design system with glassmorphism), JavaScript (ES6+), Google Fonts (Outfit) |
| **Backend** | Python 3.12, Flask 3.1.3 |
| **AI / Machine Learning** | TensorFlow / Keras (MobileNetV2 Transfer Learning), Pillow, NumPy |
| **Weather & Geocoding** | Open-Meteo Geocoding & Weather Forecast API (No API key required) |
| **Deployment** | WSGI / Gunicorn / Flask dev server |

---

## 📊 Main User Flow

```
Farmer Opens Website 
       ↓
Selects Crop (e.g. Tomato)
       ↓
Uploads Leaf Photo (Drag-and-Drop / File Picker)
       ↓
Enters Village/City or Clicks "📍 Use My Location"
       ↓
Clicks "Analyze Crop"
       ↓
AI Analyzes Image (224x224 MobileNetV2 -> Disease + Confidence %)
       ↓
Live Open-Meteo Weather & 24h Forecast Retrieved
       ↓
Climate/Disease Risk Engine Evaluates Risk Level (LOW / MEDIUM / HIGH)
       ↓
Dynamic Result Dashboard Displays Actionable Advisory + Best Time to Act
```

---

## 📁 Folder Structure

```
AgriAI_Advisor/
├── app.py                     # Flask main server application & API routes
├── requirements.txt           # Python dependency specifications
├── README.md                  # Comprehensive project documentation
├── .gitignore                 # Git ignore rules
│
├── model/
│   ├── disease_model.keras    # Trained MobileNetV2 Keras model
│   └── class_names.json       # PlantVillage class name index mapping
│
├── dataset/
│   └── PlantVillage/          # PlantVillage dataset directory
│
├── notebooks/
│   ├── train_model.ipynb      # Complete training pipeline notebook
│   └── export_model.py        # Model build & initialization helper
│
├── services/
│   ├── __init__.py            # Services package init
│   ├── disease_detection.py   # AI inference & preprocessing handler
│   ├── weather_service.py     # Open-Meteo geocoding & forecast client
│   └── advisory_service.py    # Climate-risk matrix & advisory engine
│
├── templates/
│   ├── index.html             # Single-page landing & analysis dashboard template
│   └── result.html            # Standalone result view template
│
└── static/
    ├── css/
    │   └── style.css          # Custom agricultural green design system CSS
    ├── js/
    │   └── script.js          # Client interactive logic & I18N dictionary
    └── uploads/               # Secure uploaded leaf images directory
```

---

## ⚙️ Installation & Setup Guide

### 1. Clone & Enter Workspace
```bash
cd c:/Users/User/OneDrive/Desktop/AgriAI_Advisor
```

### 2. Set Up Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Build / Export Initial MobileNetV2 Model
To compile and save `model/disease_model.keras`:
```bash
python notebooks/export_model.py
```

### 5. Run the Flask Web Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🧪 How Model Training Works (PlantVillage Dataset)

The model relies on transfer learning with **MobileNetV2** pretrained on ImageNet:
1. Base MobileNetV2 weights are frozen (`trainable = False`).
2. Custom top classification head is appended: `GlobalAveragePooling2D -> Dropout(0.2) -> Dense(num_classes, softmax)`.
3. Input leaf images are resized to `224x224` and normalized to `[-1, 1]`.
4. Run `notebooks/train_model.ipynb` or execute custom fine-tuning scripts on the PlantVillage dataset directory.

---

## 🌦️ How Open-Meteo Weather Integration Works

1. **Geocoding**: User inputs location (e.g., "Vijayawada"). The service calls:
   `https://geocoding-api.open-meteo.com/v1/search?name=Vijayawada&count=1&language=en&format=json`
2. **Forecast**: Converts `(latitude, longitude)` into weather metrics:
   `https://api.open-meteo.com/v1/forecast?latitude=16.5062&longitude=80.6480&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&hourly=precipitation_probability...`
3. **Risk Matrix**: If humidity > 75% and 24h rain probability > 60% for a moisture-susceptible pathogen (e.g. Late Blight), risk is calculated as **HIGH**.

---

## 🔒 Security & Safety Guidelines

- Uploaded filenames are sanitized using `werkzeug.utils.secure_filename`.
- Allowed upload extensions are strictly restricted to `.jpg`, `.jpeg`, `.png`, `.webp`.
- Maximum upload size is enforced at `10MB`.
- **Extension Safety**: Chemical treatment guidance excludes unverified toxic dosage instructions and includes explicit warning: *"Follow the product label and local agricultural extension guidance."*

---

## 🔮 Future Enhancements

- Edge deployment with TensorFlow Lite (TFLite) for offline mobile field scanning.
- Push notification SMS alerts for sudden high-humidity rain warnings.
- Soil sensor IoT integration via MQTT.

---

*Developed for the Agriculture & Climate Resilience Hackathon.*
