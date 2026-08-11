/* ==========================================================================
   AgriAI Advisor - Frontend Client Interactivity Script
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initLanguageSelector();
  initImageUpload();
  initGeolocation();
  initDemoToggle();
  initFormSubmission();
});

// Internationalization Dictionary (English, Telugu, Hindi)
const I18N_DICTIONARY = {
  en: {
    hero_title: "From Field Conditions to <span>Smart Farming Decisions</span>.",
    hero_sub: "Real-time AI crop disease diagnosis combined with hyper-local weather risk intelligence to protect farmer livelihoods.",
    cta_analyze: "Analyze Your Crop",
    nav_home: "Home",
    nav_how: "How It Works",
    nav_features: "Features",
    nav_about: "About",
    section_title_analyze: "Analyze Your Crop Health",
    crop_label: "🌱 Select Crop",
    loc_label: "📍 Location",
    upload_label: "📷 Upload Leaf Image",
    dropzone_title: "Upload a clear photo of the affected leaf",
    dropzone_sub: "Supports JPG, JPEG, PNG, WEBP (Max 10MB)",
    btn_analyze_text: "Analyze Crop & Check Weather",
    loading_text: "Analyzing your crop and checking local weather...",
    risk_low: "LOW RISK",
    risk_medium: "MEDIUM RISK",
    risk_high: "HIGH RISK",
    whats_wrong_title: "What's Wrong?",
    what_to_do_title: "What Should I Do?",
    prevention_title: "Prevention Steps",
    weather_warn_title: "Weather Warning",
    best_time_title: "⏰ Best Time to Act",
    weather_risk_title: "Weather-based Risk Assessment"
  },
  te: {
    hero_title: "చేను పరిస్థితుల నుండి <span>తెలివైన వ్యవసాయ నిర్ణయాల వరకు</span>.",
    hero_sub: "రైతుల జీవనోపాధిని కాపాడటానికి స్థానిక వాతావరణ సమాచారంతో కూడిన AI పంట వ్యాధి నిర్ధారణ.",
    cta_analyze: "మీ పంటను విశ్లేషించండి",
    nav_home: "హోమ్",
    nav_how: "ఇది ఎలా పనిచేస్తుంది",
    nav_features: "లక్షణాలు",
    nav_about: "గురించి",
    section_title_analyze: "మీ పంట ఆరోగ్యాన్ని విశ్లేషించండి",
    crop_label: "🌱 పంటను ఎంచుకోండి",
    loc_label: "📍 ప్రదేశం",
    upload_label: "📷 ఆకు ఫోటో అప్‌లోడ్ చేయండి",
    dropzone_title: "ప్రభావిత ఆకు యొక్క స్పష్టమైన ఫోటోను అప్‌లోడ్ చేయండి",
    dropzone_sub: "JPG, JPEG, PNG, WEBP (గరిష్టంగా 10MB)",
    btn_analyze_text: "పంటను విశ్లేషించండి మరియు వాతావరణం చూడండి",
    loading_text: "మీ పంటను విశ్లేషిస్తోంది మరియు వాతావరణాన్ని తనిఖీ చేస్తోంది...",
    risk_low: "తక్కువ ప్రమాదం",
    risk_medium: "మధ్యస్థ ప్రమాదం",
    risk_high: "అధిక ప్రమాదం",
    whats_wrong_title: "సమస్య ఏమిటి?",
    what_to_do_title: "నేను ఏమి చేయాలి?",
    prevention_title: "నివారణ చర్యలు",
    weather_warn_title: "వాతావరణ హెచ్చరిక",
    best_time_title: "⏰ చర్య తీసుకోవడానికి ఉత్తమ సమయం",
    weather_risk_title: "వాతావరణ ఆధారిత ప్రమాద అంచనా"
  },
  hi: {
    hero_title: "खेत की स्थिति से <span>स्मार्ट कृषि निर्णयों तक</span>।",
    hero_sub: "किसानों की आजीविका की सुरक्षा के लिए रीयल-टाइम AI फसल रोग निदान और स्थानीय मौसम जोखिम विश्लेषण।",
    cta_analyze: "अपनी फसल का विश्लेषण करें",
    nav_home: "होम",
    nav_how: "यह कैसे काम करता है",
    nav_features: "विशेषताएं",
    nav_about: "हमारे बारे में",
    section_title_analyze: "अपनी फसल के स्वास्थ्य का विश्लेषण करें",
    crop_label: "🌱 फसल चुनें",
    loc_label: "📍 स्थान",
    upload_label: "📷 पत्ती की फोटो अपलोड करें",
    dropzone_title: "प्रभावित पत्ती की स्पष्ट फोटो अपलोड करें",
    dropzone_sub: "JPG, JPEG, PNG, WEBP (अधिकतम 10MB)",
    btn_analyze_text: "फसल विश्लेषण और मौसम की जांच करें",
    loading_text: "आपकी फसल का विश्लेषण और स्थानीय मौसम की जांच की जा रही है...",
    risk_low: "कम जोखिम",
    risk_medium: "मध्यम जोखिम",
    risk_high: "उच्च जोखिम",
    whats_wrong_title: "क्या खराबी है?",
    what_to_do_title: "मुझे क्या करना चाहिए?",
    prevention_title: "रोकथाम के उपाय",
    weather_warn_title: "मौसम की चेतावनी",
    best_time_title: "⏰ कार्रवाई का सबसे अच्छा समय",
    weather_risk_title: "मौसम आधारित जोखिम मूल्यांकन"
  }
};

let currentLang = 'en';
let userCoords = null;

// 1. Language Selector Handler
function initLanguageSelector() {
  const langSelect = document.getElementById('langSelect');
  if (!langSelect) return;
  
  langSelect.addEventListener('change', (e) => {
    currentLang = e.target.value;
    applyLanguage(currentLang);
  });
}

function applyLanguage(lang) {
  const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY['en'];
  
  document.querySelectorAll('[data-i18n]').forEach(elem => {
    const key = elem.getAttribute('data-i18n');
    if (dict[key]) {
      elem.innerHTML = dict[key];
    }
  });
}

// 2. Drag & Drop Image Upload Handler
function initImageUpload() {
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('imageInput');
  const previewContainer = document.getElementById('previewContainer');
  const previewImage = document.getElementById('previewImage');
  const removeBtn = document.getElementById('removePreviewBtn');

  if (!dropzone || !fileInput) return;

  dropzone.addEventListener('click', () => fileInput.click());

  ['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropzone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropzone.classList.remove('dragover');
    });
  });

  dropzone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      fileInput.files = files;
      handleFileSelected(files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  if (removeBtn) {
    removeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      fileInput.value = '';
      previewContainer.style.display = 'none';
      dropzone.style.display = 'block';
    });
  }

  function handleFileSelected(file) {
    const allowed = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!allowed.includes(file.type)) {
      alert("Please upload a valid leaf image (JPG, JPEG, PNG, or WEBP).");
      fileInput.value = '';
      return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
      alert("File size exceeds 10MB limit.");
      fileInput.value = '';
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
      dropzone.style.display = 'none';
      previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
}

// 3. Geolocation Handler
function initGeolocation() {
  const gpsBtn = document.getElementById('gpsBtn');
  const locationInput = document.getElementById('locationInput');

  if (!gpsBtn) return;

  gpsBtn.addEventListener('click', () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }

    gpsBtn.innerText = "⌛ Detecting...";
    navigator.geolocation.getCurrentPosition(
      (position) => {
        userCoords = {
          lat: position.coords.latitude,
          lon: position.coords.longitude
        };
        gpsBtn.innerText = "✅ Located";
        if (locationInput && !locationInput.value) {
          locationInput.value = `GPS (${userCoords.lat.toFixed(2)}, ${userCoords.lon.toFixed(2)})`;
        }
      },
      (error) => {
        console.warn("GPS Location error:", error);
        gpsBtn.innerText = "📍 GPS Failed";
        alert("Could not fetch GPS location. Please enter your village/city manually.");
      },
      { timeout: 8000 }
    );
  });
}

// 4. Demo Mode Toggle
function initDemoToggle() {
  const demoToggle = document.getElementById('demoToggle');
  const dropzone = document.getElementById('dropzone');
  const previewContainer = document.getElementById('previewContainer');
  const previewImage = document.getElementById('previewImage');

  if (!demoToggle) return;

  demoToggle.addEventListener('change', (e) => {
    if (e.target.checked) {
      previewImage.src = "https://images.unsplash.com/photo-1592417817098-8f3d6eb1b7a5?w=500&auto=format&fit=crop&q=60";
      dropzone.style.display = 'none';
      previewContainer.style.display = 'block';
      const locInput = document.getElementById('locationInput');
      if (locInput && !locInput.value) {
        locInput.value = "Vijayawada";
      }
    }
  });
}

// 5. Form Submission & API Fetching
function initFormSubmission() {
  const form = document.getElementById('analysisForm');
  const loadingOverlay = document.getElementById('loadingOverlay');
  const resultsSection = document.getElementById('resultsSection');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('imageInput');
    const demoToggle = document.getElementById('demoToggle');
    const locationInput = document.getElementById('locationInput');

    const isDemo = demoToggle ? demoToggle.checked : false;

    if (!isDemo && (!fileInput.files || fileInput.files.length === 0)) {
      alert("Please upload a crop leaf image before analyzing.");
      return;
    }

    // Show loading
    form.style.display = 'none';
    loadingOverlay.style.display = 'block';
    resultsSection.style.display = 'none';

    const formData = new FormData(form);
    if (userCoords) {
      formData.append('lat', userCoords.lat);
      formData.append('lon', userCoords.lon);
    }
    if (isDemo) {
      formData.append('is_demo', 'true');
    }

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      loadingOverlay.style.display = 'none';
      form.style.display = 'block';

      if (response.ok && data.status === 'success') {
        renderResultsDashboard(data);
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
      } else {
        alert(data.message || "An error occurred during crop analysis.");
      }
    } catch (err) {
      console.error("Analysis request error:", err);
      loadingOverlay.style.display = 'none';
      form.style.display = 'block';
      alert("Failed to connect to AgriAI Advisor server. Please check your internet connection.");
    }
  });
}

// 6. Render Results Dashboard
function renderResultsDashboard(data) {
  const dict = I18N_DICTIONARY[currentLang] || I18N_DICTIONARY['en'];

  // Banner elements
  const resImage = document.getElementById('resImage');
  const resCropDiseaseTitle = document.getElementById('resCropDiseaseTitle');
  const resLocationMeta = document.getElementById('resLocationMeta');
  const resRiskBadge = document.getElementById('resRiskBadge');
  const resDemoLabel = document.getElementById('resDemoLabel');

  if (resImage) resImage.src = data.image_url || 'https://images.unsplash.com/photo-1592417817098-8f3d6eb1b7a5?w=500&auto=format&fit=crop&q=60';
  if (resCropDiseaseTitle) resCropDiseaseTitle.innerText = `${data.crop} - ${data.disease.disease_name}`;
  if (resLocationMeta) resLocationMeta.innerText = `Location: ${data.weather.location_name} | AI Confidence: ${data.disease.confidence}%`;

  if (resDemoLabel) {
    resDemoLabel.innerText = data.is_demo ? "Demo Mode Active" : "";
    resDemoLabel.style.display = data.is_demo ? "inline-block" : "none";
  }

  // Risk Badge styling
  if (resRiskBadge) {
    resRiskBadge.className = `risk-badge ${data.advisory.risk_badge}`;
    const riskText = data.advisory.risk_level === "HIGH" ? dict.risk_high :
                     (data.advisory.risk_level === "MEDIUM" ? dict.risk_medium : dict.risk_low);
    resRiskBadge.innerText = `⚠️ ${riskText}`;
  }

  // Stat Pills
  document.getElementById('valCropType').innerText = data.crop;
  document.getElementById('valDetectedDisease').innerText = data.disease.disease_name;
  document.getElementById('valConfidenceScore').innerText = `${data.disease.confidence}%`;
  
  // Low confidence notice
  const lowConfAlert = document.getElementById('lowConfidenceAlert');
  if (lowConfAlert) {
    if (data.disease.is_low_confidence) {
      lowConfAlert.style.display = 'flex';
      lowConfAlert.innerText = `⚠️ ${data.disease.confidence_message}`;
    } else {
      lowConfAlert.style.display = 'none';
    }
  }

  // Weather Metrics
  const w = data.weather.current;
  document.getElementById('valTemp').innerText = `${w.temperature}°C`;
  document.getElementById('valHumidity').innerText = `${w.humidity}%`;
  document.getElementById('valRainProb').innerText = `${w.rain_probability}%`;
  document.getElementById('valWindSpeed').innerText = `${w.wind_speed} km/h`;
  document.getElementById('valCondition').innerText = `${w.icon} ${w.condition}`;

  // Hourly Forecast Strip
  const hourlyStrip = document.getElementById('hourlyForecastStrip');
  if (hourlyStrip && data.weather.forecast_24h) {
    hourlyStrip.innerHTML = data.weather.forecast_24h.map(h => `
      <div class="hourly-box">
        <div class="hourly-time">${h.time}</div>
        <div class="hourly-temp">${h.temp}°C</div>
        <div class="hourly-rain">🌧️ ${h.rain_prob}%</div>
      </div>
    `).join('');
  }

  // Weather-based Risk Assessment
  const riskAssessText = document.getElementById('valWeatherRiskText');
  if (riskAssessText) {
    riskAssessText.innerText = data.advisory.weather_risk_assessment;
  }

  // Advisory Cards
  document.getElementById('valWhatsWrong').innerText = data.advisory.whats_wrong;
  document.getElementById('valWhatToDo').innerText = data.advisory.what_should_i_do;
  document.getElementById('valPrevention').innerText = data.advisory.prevention;
  document.getElementById('valWeatherWarning').innerText = data.advisory.weather_warning;

  // Best Time to Act Card
  const btta = data.advisory.best_time_to_act;
  const bttaTitle = document.getElementById('valBestTimeTitle');
  const bttaBody = document.getElementById('valBestTimeBody');
  const bttaNotice = document.getElementById('valPesticideNotice');

  if (bttaTitle) bttaTitle.innerText = `${btta.status_icon} ${btta.title}`;
  if (bttaBody) bttaBody.innerText = btta.recommendation;
  if (bttaNotice) bttaNotice.innerText = `📌 Note: ${data.advisory.pesticide_notice}`;
}
