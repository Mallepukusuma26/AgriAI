import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WMO Weather Interpretation Codes mapping to description & icon
WMO_CODES = {
    0: {"desc": "Clear Sky", "icon": "☀️"},
    1: {"desc": "Mainly Clear", "icon": "🌤️"},
    2: {"desc": "Partly Cloudy", "icon": "⛅"},
    3: {"desc": "Overcast", "icon": "☁️"},
    45: {"desc": "Foggy", "icon": "🌫️"},
    48: {"desc": "Depositing Rime Fog", "icon": "🌫️"},
    51: {"desc": "Light Drizzle", "icon": "🌧️"},
    53: {"desc": "Moderate Drizzle", "icon": "🌧️"},
    55: {"desc": "Dense Drizzle", "icon": "🌧️"},
    61: {"desc": "Slight Rain", "icon": "🌧️"},
    63: {"desc": "Moderate Rain", "icon": "🌧️"},
    65: {"desc": "Heavy Rain", "icon": "⛈️"},
    71: {"desc": "Slight Snow", "icon": "🌨️"},
    73: {"desc": "Moderate Snow", "icon": "🌨️"},
    75: {"desc": "Heavy Snow", "icon": "🌨️"},
    80: {"desc": "Slight Rain Showers", "icon": "🌦️"},
    81: {"desc": "Moderate Rain Showers", "icon": "🌦️"},
    82: {"desc": "Violent Rain Showers", "icon": "⛈️"},
    95: {"desc": "Thunderstorm", "icon": "⛈️"},
    96: {"desc": "Thunderstorm with Hail", "icon": "⛈️"}
}


def geocode_location(location_name):
    """
    Converts city/village string into latitude and longitude using Open-Meteo Geocoding API.
    """
    try:
        params = {
            "name": location_name,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        response = requests.get(GEOCODING_URL, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                top = data["results"][0]
                return {
                    "found": True,
                    "name": top.get("name", location_name),
                    "country": top.get("country", ""),
                    "admin1": top.get("admin1", ""),
                    "lat": round(top["latitude"], 4),
                    "lon": round(top["longitude"], 4)
                }
    except Exception as e:
        print(f"Geocoding error for '{location_name}': {e}")
    
    # Fallback default (Vijayawada, AP, India)
    return {
        "found": False,
        "name": location_name if location_name else "Vijayawada",
        "country": "India",
        "admin1": "Andhra Pradesh",
        "lat": 16.5062,
        "lon": 80.6480
    }


def get_weather_and_forecast(lat, lon, location_name="Local Area"):
    """
    Retrieves live weather data and multi-day forecast from Open-Meteo API.
    """
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m",
            "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,rain,weather_code",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
            "timezone": "auto"
        }
        resp = requests.get(FORECAST_URL, params=params, timeout=6)
        if resp.status_code == 200:
            data = resp.json()
            
            # Current conditions
            current = data.get("current", {})
            code = current.get("weather_code", 0)
            wmo_info = WMO_CODES.get(code, {"desc": "Partly Cloudy", "icon": "⛅"})
            
            hourly = data.get("hourly", {})
            hourly_times = hourly.get("time", [])[:24]
            hourly_temps = hourly.get("temperature_2m", [])[:24]
            hourly_rain_prob = hourly.get("precipitation_probability", [])[:24]
            
            # Calculate max rain probability in next 24h
            next_24h_rain_prob = max(hourly_rain_prob) if hourly_rain_prob else 0
            
            daily = data.get("daily", {})
            daily_times = daily.get("time", [])[:7]
            daily_max_temp = daily.get("temperature_2m_max", [])[:7]
            daily_min_temp = daily.get("temperature_2m_min", [])[:7]
            daily_rain_sum = daily.get("precipitation_sum", [])[:7]
            daily_rain_prob = daily.get("precipitation_probability_max", [])[:7]
            
            forecast_24h = []
            for i in range(min(24, len(hourly_times))):
                time_str = hourly_times[i].split("T")[-1] if "T" in hourly_times[i] else str(i)
                forecast_24h.append({
                    "time": time_str,
                    "temp": round(hourly_temps[i], 1) if i < len(hourly_temps) else 0,
                    "rain_prob": hourly_rain_prob[i] if i < len(hourly_rain_prob) else 0
                })
                
            forecast_7day = []
            for i in range(min(7, len(daily_times))):
                forecast_7day.append({
                    "date": daily_times[i],
                    "max_temp": daily_max_temp[i] if i < len(daily_max_temp) else 0,
                    "min_temp": daily_min_temp[i] if i < len(daily_min_temp) else 0,
                    "rain_sum": daily_rain_sum[i] if i < len(daily_rain_sum) else 0,
                    "rain_prob": daily_rain_prob[i] if i < len(daily_rain_prob) else 0
                })

            return {
                "status": "success",
                "location_name": location_name,
                "lat": lat,
                "lon": lon,
                "current": {
                    "temperature": round(current.get("temperature_2m", 28.5), 1),
                    "humidity": current.get("relative_humidity_2m", 78),
                    "precipitation": round(current.get("precipitation", 0.0), 1),
                    "wind_speed": round(current.get("wind_speed_10m", 12.0), 1),
                    "rain_probability": next_24h_rain_prob,
                    "condition": wmo_info["desc"],
                    "icon": wmo_info["icon"]
                },
                "forecast_24h": forecast_24h,
                "forecast_7day": forecast_7day
            }
    except Exception as e:
        print(f"Weather API error: {e}")
        
    # Return realistic offline fallback weather data
    return get_fallback_weather(location_name, lat, lon)


def get_fallback_weather(location_name="Vijayawada", lat=16.5062, lon=80.6480):
    """
    Structured fallback dataset when Open-Meteo API is offline or unreachable.
    """
    return {
        "status": "fallback",
        "location_name": location_name,
        "lat": lat,
        "lon": lon,
        "current": {
            "temperature": 29.0,
            "humidity": 84,
            "precipitation": 3.2,
            "wind_speed": 14.5,
            "rain_probability": 72,
            "condition": "Moderate Rain",
            "icon": "🌧️"
        },
        "forecast_24h": [
            {"time": "00:00", "temp": 27.5, "rain_prob": 65},
            {"time": "04:00", "temp": 26.8, "rain_prob": 75},
            {"time": "08:00", "temp": 28.2, "rain_prob": 70},
            {"time": "12:00", "temp": 30.5, "rain_prob": 40},
            {"time": "16:00", "temp": 29.8, "rain_prob": 55},
            {"time": "20:00", "temp": 28.0, "rain_prob": 60}
        ],
        "forecast_7day": [
            {"date": "Today", "max_temp": 30.5, "min_temp": 26.5, "rain_sum": 3.2, "rain_prob": 72},
            {"date": "Tomorrow", "max_temp": 31.0, "min_temp": 25.8, "rain_sum": 1.5, "rain_prob": 45},
            {"date": "Day 3", "max_temp": 32.2, "min_temp": 26.0, "rain_sum": 0.0, "rain_prob": 15},
            {"date": "Day 4", "max_temp": 33.0, "min_temp": 26.5, "rain_sum": 0.0, "rain_prob": 10},
            {"date": "Day 5", "max_temp": 32.5, "min_temp": 27.0, "rain_sum": 0.5, "rain_prob": 25}
        ]
    }
