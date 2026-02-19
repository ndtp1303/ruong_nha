import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherAPI:
    """Handle OpenWeatherMap API calls with caching"""
    
    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # Vietnam province coordinates (major cities in Mekong Delta)
        self.coordinates = {
            "An Giang": {"lat": 10.5216, "lon": 105.1258},
            "Bạc Liêu": {"lat": 9.2940, "lon": 105.7215},
            "Bến Tre": {"lat": 10.2433, "lon": 106.3757},
            "Cà Mau": {"lat": 9.1526, "lon": 105.1960},
            "Cần Thơ": {"lat": 10.0452, "lon": 105.7469},
            "Đồng Tháp": {"lat": 10.4938, "lon": 105.6881},
            "Hậu Giang": {"lat": 9.7577, "lon": 105.4707},
            "Kiên Giang": {"lat": 10.0125, "lon": 105.0808},
            "Long An": {"lat": 10.6956, "lon": 106.2431},
            "Sóc Trăng": {"lat": 9.6037, "lon": 105.9740},
            "Tiền Giang": {"lat": 10.4493, "lon": 106.3420},
            "Trà Vinh": {"lat": 9.8124, "lon": 106.2992},
            "Vĩnh Long": {"lat": 10.2395, "lon": 105.9571}
        }
    
    def get_current_weather(self, province: str) -> Optional[Dict]:
        """Get current weather for a province"""
        if not self.api_key or self.api_key == "your_openweathermap_api_key_here":
            return None

        coords = self.coordinates.get(province)
        if not coords:
            return None

        # Check cache
        cache_key = f"weather_current_{province}"
        if cache_key in st.session_state:
            cached_data, cached_time = st.session_state[cache_key]
            if datetime.now() - cached_time < timedelta(minutes=30):
                return cached_data

        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": coords["lat"],
                "lon": coords["lon"],
                "appid": self.api_key,
                "units": "metric",
                "lang": "vi"
            }

            response = requests.get(url, params=params, timeout=10)

            # Check for API errors
            if response.status_code == 401:
                st.error("⚠️ API key không hợp lệ hoặc chưa được kích hoạt. Vui lòng đợi 1-2 giờ sau khi đăng ký.")
                return None
            elif response.status_code != 200:
                st.warning(f"⚠️ Lỗi API: {response.status_code} - {response.text[:100]}")
                return None

            response.raise_for_status()
            data = response.json()

            # Cache the result
            st.session_state[cache_key] = (data, datetime.now())
            return data

        except requests.exceptions.Timeout:
            st.warning("⚠️ Timeout khi kết nối API thời tiết")
            return None
        except requests.exceptions.RequestException as e:
            st.warning(f"⚠️ Lỗi kết nối: {str(e)[:100]}")
            return None
        except Exception as e:
            print(f"Weather API error: {e}")
            return None
    
    def get_forecast(self, province: str) -> Optional[List[Dict]]:
        """Get 7-day forecast for a province"""
        if not self.api_key or self.api_key == "your_openweathermap_api_key_here":
            return None

        coords = self.coordinates.get(province)
        if not coords:
            return None

        # Check cache
        cache_key = f"weather_forecast_{province}"
        if cache_key in st.session_state:
            cached_data, cached_time = st.session_state[cache_key]
            if datetime.now() - cached_time < timedelta(minutes=30):
                return cached_data

        try:
            url = f"{self.base_url}/forecast"
            params = {
                "lat": coords["lat"],
                "lon": coords["lon"],
                "appid": self.api_key,
                "units": "metric",
                "lang": "vi",
                "cnt": 40  # 5 days * 8 (3-hour intervals)
            }

            response = requests.get(url, params=params, timeout=10)

            # Check for API errors
            if response.status_code == 401:
                return None  # Already showed error in get_current_weather
            elif response.status_code != 200:
                return None

            response.raise_for_status()
            data = response.json()

            # Process forecast data - group by day
            daily_forecast = self._process_forecast(data)

            # Cache the result
            st.session_state[cache_key] = (daily_forecast, datetime.now())
            return daily_forecast

        except Exception as e:
            print(f"Forecast API error: {e}")
            return None
    
    def _process_forecast(self, data: Dict) -> List[Dict]:
        """Process forecast data into daily summaries"""
        daily_data = {}
        
        for item in data.get("list", []):
            date = datetime.fromtimestamp(item["dt"]).strftime("%d/%m")
            
            if date not in daily_data:
                daily_data[date] = {
                    "temps": [],
                    "rain_prob": [],
                    "humidity": []
                }
            
            daily_data[date]["temps"].append(item["main"]["temp"])
            daily_data[date]["rain_prob"].append(item.get("pop", 0) * 100)
            daily_data[date]["humidity"].append(item["main"]["humidity"])
        
        # Calculate daily averages
        result = []
        for date, values in list(daily_data.items())[:7]:  # Only 7 days
            result.append({
                "date": date,
                "temp_high": max(values["temps"]),
                "temp_low": min(values["temps"]),
                "rain_chance": max(values["rain_prob"]),
                "humidity": sum(values["humidity"]) / len(values["humidity"])
            })
        
        return result

