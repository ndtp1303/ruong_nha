from datetime import datetime, timedelta
from typing import List, Tuple
import math

class SalinityCalculator:
    """Calculate salinity predictions based on season, location, and weather"""
    
    # Coastal provinces have higher base salinity
    COASTAL_PROVINCES = ["Bạc Liêu", "Cà Mau", "Kiên Giang", "Sóc Trăng", "Trà Vinh", "Bến Tre"]
    
    # Dry season months (higher salinity)
    DRY_SEASON_MONTHS = [1, 2, 3, 4, 5]  # Jan-May
    
    def __init__(self):
        pass
    
    def get_base_salinity(self, province: str, month: int) -> float:
        """Calculate base salinity based on province and month"""
        base = 2.0  # Default base salinity
        
        # Coastal areas have higher salinity
        if province in self.COASTAL_PROVINCES:
            base += 1.5
        
        # Dry season increases salinity
        if month in self.DRY_SEASON_MONTHS:
            # Peak in March-April
            if month in [3, 4]:
                base += 2.0
            elif month in [2, 5]:
                base += 1.5
            else:  # January
                base += 1.0
        else:
            # Rainy season (June-December) reduces salinity
            base -= 0.5
        
        return max(0.5, base)  # Minimum 0.5‰
    
    def calculate_current_salinity(self, province: str, recent_rainfall: float = 0) -> float:
        """Calculate current salinity level"""
        current_month = datetime.now().month
        base_salinity = self.get_base_salinity(province, current_month)
        
        # Recent rainfall reduces salinity
        if recent_rainfall > 50:  # Heavy rain
            base_salinity -= 1.0
        elif recent_rainfall > 20:  # Moderate rain
            base_salinity -= 0.5
        
        return max(0.5, round(base_salinity, 1))
    
    def forecast_salinity(self, province: str, days: int = 14) -> List[Tuple[str, float]]:
        """Forecast salinity for next N days"""
        current_date = datetime.now()
        current_salinity = self.calculate_current_salinity(province)
        
        forecast = []
        
        for i in range(days):
            date = current_date + timedelta(days=i)
            date_str = date.strftime("%d/%m")
            
            # Calculate trend
            month = date.month
            day_of_month = date.day
            
            # Salinity increases during dry season, peaks mid-month
            if month in self.DRY_SEASON_MONTHS:
                # Simulate increase towards mid-month
                if day_of_month < 15:
                    trend = 0.1 * (day_of_month / 15)
                else:
                    trend = 0.1 * ((30 - day_of_month) / 15)
            else:
                # Rainy season - gradual decrease
                trend = -0.05
            
            # Add some variation
            variation = math.sin(i * 0.5) * 0.2
            
            salinity = current_salinity + (i * trend) + variation
            salinity = max(0.5, min(8.0, round(salinity, 1)))  # Clamp between 0.5-8.0
            
            forecast.append((date_str, salinity))
        
        return forecast
    
    def get_salinity_level(self, salinity: float) -> Tuple[str, str]:
        """Get salinity warning level and color"""
        if salinity < 2.0:
            return "An toàn", "green"
        elif salinity < 4.0:
            return "Trung bình", "orange"
        else:
            return "Cao", "red"
    
    def get_recommendations(self, salinity: float, forecast_max: float) -> List[str]:
        """Get recommendations based on salinity levels"""
        recommendations = []
        
        if salinity < 2.0:
            recommendations.append("✓ Điều kiện tốt cho hầu hết các giống lúa")
            recommendations.append("✓ Có thể trồng rau màu, cây ăn trái")
        elif salinity < 4.0:
            recommendations.append("⚠ Nên chọn giống lúa chịu mặn vừa (OM 9577, OM 9582)")
            recommendations.append("⚠ Tăng mực nước trong ruộng")
            recommendations.append("⚠ Theo dõi tình trạng cây trồng thường xuyên")
        else:
            recommendations.append("🚨 Độ mặn cao - Cần hành động ngay")
            recommendations.append("🚨 Chọn giống chịu mặn tốt (OM 9676)")
            recommendations.append("🚨 Cân nhắc chuyển sang mô hình lúa-tôm")
            recommendations.append("🚨 Liên hệ chuyên gia thủy lợi")
        
        # Future warnings
        if forecast_max > salinity + 1.0:
            recommendations.append(f"⚠ Cảnh báo: Độ mặn dự báo tăng lên {forecast_max}‰")
            recommendations.append("→ Tích trữ nước ngọt trước khi độ mặn tăng")
        
        return recommendations

