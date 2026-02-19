import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.weather_api import WeatherAPI
from utils.salinity_calculator import SalinityCalculator

weather_api = WeatherAPI()
salinity_calc = SalinityCalculator()

theme = st.session_state.get("theme", "light")

if theme == "light":
    st.markdown("""
    <style>
        .utility-header {
            text-align: center;
            padding: 2rem 0;
            border-bottom: 1px solid #dee2e6;
            margin-bottom: 2rem;
        }

        .utility-title {
            font-size: 2rem;
            font-weight: 600;
            color: #2d6a4f;
            margin-bottom: 0.5rem;
        }

        .utility-subtitle {
            font-size: 1rem;
            color: #495057;
        }

        .metric-card {
            background: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #212529;
        }

        .metric-label {
            font-size: 0.875rem;
            color: #6c757d;
            margin-top: 0.25rem;
        }

        .alert-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 1rem 1.5rem;
            border-radius: 4px;
            margin: 1rem 0;
        }

        .danger-box {
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 1rem 1.5rem;
            border-radius: 4px;
            margin: 1rem 0;
        }

        .info-box {
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 1rem 1.5rem;
            border-radius: 4px;
            margin: 1rem 0;
        }

        .recommendation-section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #dee2e6;
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .utility-header {
            text-align: center;
            padding: 2rem 0;
            border-bottom: 1px solid #3d4349;
            margin-bottom: 2rem;
        }

        .utility-title {
            font-size: 2rem;
            font-weight: 600;
            color: #52b788;
            margin-bottom: 0.5rem;
        }

        .utility-subtitle {
            font-size: 1rem;
            color: #b8bdc3;
        }

        .metric-card {
            background: #1a1f26;
            border: 1px solid #3d4349;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #e8eaed;
        }

        .metric-label {
            font-size: 0.875rem;
            color: #b8bdc3;
            margin-top: 0.25rem;
        }

        .alert-box {
            background: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #ffc107;
            padding: 1rem 1.5rem;
            border-radius: 4px;
            margin: 1rem 0;
            border: 1px solid rgba(255, 193, 7, 0.2);
        }

        .danger-box {
            background: rgba(220, 53, 69, 0.1);
            border-left: 4px solid #dc3545;
            padding: 1rem 1.5rem;
            border-radius: 4px;
            margin: 1rem 0;
            border: 1px solid rgba(220, 53, 69, 0.2);
        }

        .info-box {
            background: rgba(23, 162, 184, 0.1);
            border-left: 4px solid #17a2b8;
            padding: 1rem 1.5rem;
            border-radius: 4px;
            margin: 1rem 0;
            border: 1px solid rgba(23, 162, 184, 0.2);
        }

        .recommendation-section {
            background: #1a1f26;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #3d4349;
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class='utility-header'>
        <h1 class='utility-title'>Tiện Ích Nông Nghiệp</h1>
        <p class='utility-subtitle'>Thông tin thời tiết, cảnh báo mặn và gợi ý giống cây</p>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Thời tiết", "Cảnh báo mặn", "Giống cây"])

with tab1:
    st.markdown("### Dự báo thời tiết")

    col1, col2 = st.columns([2, 1])
    with col1:
        province = st.selectbox(
            "Chọn tỉnh/thành",
            ["An Giang", "Bạc Liêu", "Bến Tre", "Cà Mau", "Cần Thơ",
             "Đồng Tháp", "Hậu Giang", "Kiên Giang", "Long An",
             "Sóc Trăng", "Tiền Giang", "Trà Vinh", "Vĩnh Long"]
        )
    with col2:
        if st.button("Làm mới", use_container_width=True):
            cache_keys = [f"weather_current_{province}", f"weather_forecast_{province}"]
            for key in cache_keys:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    with st.spinner("Đang tải dữ liệu thời tiết..."):
        current_weather = weather_api.get_current_weather(province)
        forecast_data = weather_api.get_forecast(province)

    st.markdown("### Thời tiết hiện tại")

    if current_weather:
        temp = round(current_weather["main"]["temp"])
        humidity = current_weather["main"]["humidity"]
        wind_speed = round(current_weather["wind"]["speed"] * 3.6)
        rain_prob = current_weather.get("rain", {}).get("1h", 0)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{temp}°C</div>
                    <div class='metric-label'>Nhiệt độ</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{humidity}%</div>
                    <div class='metric-label'>Độ ẩm</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            rain_display = f"{round(rain_prob)}mm" if rain_prob > 0 else "0mm"
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{rain_display}</div>
                    <div class='metric-label'>Lượng mưa</div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{wind_speed} km/h</div>
                    <div class='metric-label'>Tốc độ gió</div>
                </div>
            """, unsafe_allow_html=True)

        st.caption(f"Cập nhật lúc: {datetime.now().strftime('%H:%M %d/%m/%Y')}")
    else:
        st.warning("Không thể tải dữ liệu thời tiết.")
        st.info("""
        **Nguyên nhân có thể:**
        - API key chưa được kích hoạt (cần đợi 1-2 giờ sau khi đăng ký)
        - API key không hợp lệ
        - Vượt quá giới hạn miễn phí (1000 calls/ngày)

        **Hướng dẫn:**
        1. Đăng ký tại: https://openweathermap.org/api
        2. Lấy API key từ trang My API Keys
        3. Thêm vào file .env: `WEATHER_API_KEY=your_key_here`
        4. Đợi 1-2 giờ để API key được kích hoạt
        5. Restart ứng dụng

        **Đang sử dụng dữ liệu mẫu để demo**
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Dự báo 7 ngày tới")

    if forecast_data and len(forecast_data) > 0:
        dates = [item["date"] for item in forecast_data]
        temps_high = [item["temp_high"] for item in forecast_data]
        temps_low = [item["temp_low"] for item in forecast_data]
        rain_chance = [item["rain_chance"] for item in forecast_data]

        chart_template = "plotly" if theme == "light" else "plotly_dark"

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=temps_high,
            name='Cao nhất',
            line=dict(color='#ff6b6b', width=3),
            mode='lines+markers'
        ))
        fig.add_trace(go.Scatter(
            x=dates, y=temps_low,
            name='Thấp nhất',
            line=dict(color='#4ecdc4', width=3),
            mode='lines+markers'
        ))
        fig.update_layout(
            title="Nhiệt độ (°C)",
            xaxis_title="Ngày",
            yaxis_title="Nhiệt độ (°C)",
            hovermode='x unified',
            height=300,
            template=chart_template
        )
        st.plotly_chart(fig, use_container_width=True, key="weather_temp_chart_real")

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=dates, y=rain_chance,
            marker_color='#3498db',
            name='Khả năng mưa'
        ))
        fig2.update_layout(
            title="Khả năng mưa (%)",
            xaxis_title="Ngày",
            yaxis_title="Khả năng (%)",
            height=300,
            template=chart_template
        )
        st.plotly_chart(fig2, use_container_width=True, key="weather_rain_chart_real")

        max_rain = max(rain_chance)
        if max_rain > 60:
            st.markdown(f"""
                <div class='alert-box'>
                    <strong>Cảnh báo:</strong> Khả năng mưa lớn lên đến {round(max_rain)}%. Chuẩn bị biện pháp thoát nước.
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Đang sử dụng dữ liệu mẫu. Thêm WEATHER_API_KEY để xem dữ liệu thực.")
        dates = [(datetime.now() + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
        temps_high = [33, 34, 32, 31, 33, 34, 33]
        temps_low = [25, 26, 24, 23, 25, 26, 25]
        rain_chance = [20, 30, 60, 70, 40, 20, 10]

        chart_template = "plotly" if theme == "light" else "plotly_dark"

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=temps_high,
            name='Cao nhất',
            line=dict(color='#ff6b6b', width=3),
            mode='lines+markers'
        ))
        fig.add_trace(go.Scatter(
            x=dates, y=temps_low,
            name='Thấp nhất',
            line=dict(color='#4ecdc4', width=3),
            mode='lines+markers'
        ))
        fig.update_layout(
            title="Nhiệt độ (°C)",
            xaxis_title="Ngày",
            yaxis_title="Nhiệt độ (°C)",
            hovermode='x unified',
            height=300,
            template=chart_template
        )
        st.plotly_chart(fig, use_container_width=True, key="weather_temp_chart_sample")

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=dates, y=rain_chance,
            marker_color='#3498db',
            name='Khả năng mưa'
        ))
        fig2.update_layout(
            title="Khả năng mưa (%)",
            xaxis_title="Ngày",
            yaxis_title="Khả năng (%)",
            height=300,
            template=chart_template
        )
        st.plotly_chart(fig2, use_container_width=True, key="weather_rain_chart_sample")

        st.markdown("""
            <div class='alert-box'>
                <strong>Cảnh báo:</strong> Khả năng mưa lớn vào ngày 19-20/02. Chuẩn bị biện pháp thoát nước.
            </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### Cảnh báo xâm nhập mặn")

    col1, col2 = st.columns([2, 1])
    with col1:
        salinity_province = st.selectbox(
            "Chọn tỉnh/thành",
            ["An Giang", "Bạc Liêu", "Bến Tre", "Cà Mau", "Cần Thơ",
             "Đồng Tháp", "Hậu Giang", "Kiên Giang", "Long An",
             "Sóc Trăng", "Tiền Giang", "Trà Vinh", "Vĩnh Long"],
            key="salinity_province"
        )
    with col2:
        if st.button("Làm mới", use_container_width=True, key="refresh_salinity"):
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    current_salinity = salinity_calc.calculate_current_salinity(salinity_province)
    forecast_salinity = salinity_calc.forecast_salinity(salinity_province, days=14)

    salinity_7day = [s for d, s in forecast_salinity[:7]]
    max_7day = max(salinity_7day)

    level, color = salinity_calc.get_salinity_level(current_salinity)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{current_salinity} ‰</div>
                <div class='metric-label'>Độ mặn hiện tại</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{max_7day} ‰</div>
                <div class='metric-label'>Dự báo 7 ngày</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        border_color = {"green": "#52b788", "orange": "#ffc107", "red": "#dc3545"}[color]
        text_color = {"green": "#52b788", "orange": "#ffc107", "red": "#dc3545"}[color]
        st.markdown(f"""
            <div class='metric-card' style='border-color: {border_color};'>
                <div class='metric-value' style='color: {text_color};'>{level}</div>
                <div class='metric-label'>Mức cảnh báo</div>
            </div>
        """, unsafe_allow_html=True)

    st.caption(f"Cập nhật lúc: {datetime.now().strftime('%H:%M %d/%m/%Y')}")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Dự báo độ mặn 14 ngày")

    dates_14 = [d for d, s in forecast_salinity]
    salinity_values = [s for d, s in forecast_salinity]

    chart_template = "plotly" if theme == "light" else "plotly_dark"

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=dates_14, y=salinity_values,
        fill='tozeroy',
        line=dict(color='#e74c3c', width=3),
        name='Độ mặn'
    ))

    fig3.add_hline(y=4.0, line_dash="dash", line_color="orange",
                   annotation_text="Ngưỡng cảnh báo (4‰)")
    fig3.add_hline(y=2.0, line_dash="dash", line_color="green",
                   annotation_text="Mức an toàn (2‰)")

    fig3.update_layout(
        title="Độ mặn (‰)",
        xaxis_title="Ngày",
        yaxis_title="Độ mặn (‰)",
        hovermode='x unified',
        height=400,
        template=chart_template
    )
    st.plotly_chart(fig3, use_container_width=True, key="salinity_forecast_chart")

    recommendations = salinity_calc.get_recommendations(current_salinity, max_7day)

    if max_7day > 4.0:
        st.markdown(f"""
            <div class='danger-box'>
                <strong>Cảnh báo:</strong> Độ mặn dự báo tăng cao lên {max_7day}‰
            </div>
        """, unsafe_allow_html=True)
    elif max_7day > current_salinity + 0.5:
        st.markdown(f"""
            <div class='alert-box'>
                <strong>Lưu ý:</strong> Độ mặn có xu hướng tăng từ {current_salinity}‰ lên {max_7day}‰
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class='info-box'>
                <strong>Thông tin:</strong> Độ mặn ổn định trong 7 ngày tới
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='recommendation-section'>", unsafe_allow_html=True)
    st.markdown("### Khuyến nghị")
    for rec in recommendations:
        st.markdown(f"- {rec}")
    st.markdown("</div>", unsafe_allow_html=True)

    if current_salinity > 3.0:
        if st.button("Liên hệ chuyên gia thủy lợi", use_container_width=True, type="primary"):
            st.switch_page("pages/experts.py")

with tab3:
    st.markdown("### Gợi ý giống cây trồng")

    current_month = datetime.now().month
    if current_month in [11, 12, 1, 2, 3]:
        default_season = "Đông Xuân"
    elif current_month in [4, 5, 6, 7]:
        default_season = "Hè Thu"
    else:
        default_season = "Thu Đông"

    col1, col2 = st.columns(2)
    with col1:
        soil_salinity = st.slider("Độ mặn đất (‰)", 0.0, 10.0, 3.0, 0.5)
    with col2:
        season = st.selectbox("Mùa vụ", ["Đông Xuân", "Hè Thu", "Thu Đông"],
                             index=["Đông Xuân", "Hè Thu", "Thu Đông"].index(default_season))

    st.caption(f"Mùa vụ hiện tại: {default_season} (tháng {current_month})")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Giống lúa phù hợp")

    if soil_salinity < 2.0:
        crops = [
            {"name": "OM 5451", "yield": "7-8 tấn/ha", "days": "95-100 ngày", "salinity": "< 2‰"},
            {"name": "OM 6976", "yield": "7.5-8.5 tấn/ha", "days": "90-95 ngày", "salinity": "< 2‰"},
            {"name": "Đài thơm 8", "yield": "6-7 tấn/ha", "days": "95-100 ngày", "salinity": "< 2‰"}
        ]
        st.markdown("""
            <div class='info-box'>
                <strong>Điều kiện tốt:</strong> Độ mặn thấp, phù hợp với các giống năng suất cao
            </div>
        """, unsafe_allow_html=True)
    elif soil_salinity < 4.0:
        crops = [
            {"name": "OM 9577", "yield": "6-7 tấn/ha", "days": "95-100 ngày", "salinity": "2-4‰"},
            {"name": "OM 9582", "yield": "6.5-7.5 tấn/ha", "days": "90-95 ngày", "salinity": "2-4‰"},
            {"name": "Jasmine 85", "yield": "6-7 tấn/ha", "days": "100-105 ngày", "salinity": "2-4‰"}
        ]
        st.markdown("""
            <div class='alert-box'>
                <strong>Cảnh báo:</strong> Độ mặn trung bình, nên chọn giống chịu mặn vừa
            </div>
        """, unsafe_allow_html=True)
    else:
        crops = [
            {"name": "OM 9676", "yield": "5-6 tấn/ha", "days": "95-100 ngày", "salinity": "4-6‰"},
            {"name": "OM 9577", "yield": "5-6 tấn/ha", "days": "95-100 ngày", "salinity": "4-6‰"},
            {"name": "Lúa chịu mặn địa phương", "yield": "4-5 tấn/ha", "days": "100-110 ngày", "salinity": "> 6‰"}
        ]
        st.markdown("""
            <div class='danger-box'>
                <strong>Độ mặn cao:</strong> Cần chọn giống chịu mặn tốt hoặc cân nhắc chuyển đổi mô hình
            </div>
        """, unsafe_allow_html=True)

    # Display crop table
    df = pd.DataFrame(crops)
    st.dataframe(
        df,
        column_config={
            "name": "Tên giống",
            "yield": "Năng suất",
            "days": "Thời gian",
            "salinity": "Chịu mặn"
        },
        hide_index=True,
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Alternative models
    st.markdown("### Mô hình canh tác thay thế")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("#### Lúa - Tôm")
            st.write("**Phù hợp:** Độ mặn 2-6‰")
            st.write("**Thu nhập:** 80-120 triệu/ha/năm")
            st.write("**Ưu điểm:** Đa dạng hóa thu nhập, giảm rủi ro")
            st.write("**Thời gian:** 2 vụ lúa + 1 vụ tôm")

    with col2:
        with st.container(border=True):
            st.markdown("#### Lúa - Cá")
            st.write("**Phù hợp:** Độ mặn < 2‰")
            st.write("**Thu nhập:** 70-100 triệu/ha/năm")
            st.write("**Ưu điểm:** Giảm sâu bệnh, tăng độ phì nhiêu")
            st.write("**Thời gian:** 2-3 vụ lúa + nuôi cá quanh năm")

    if st.button("Tư vấn chuyển đổi mô hình", use_container_width=True, type="primary"):
        st.switch_page("pages/ai_consultation.py")

