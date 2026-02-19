import streamlit as st
from datetime import datetime

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .welcome-box {
        background: #1a1f26;
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid #3d4349;
        margin-bottom: 2rem;
    }

    .welcome-title {
        font-size: 2rem;
        font-weight: 600;
        color: #52b788;
        margin-bottom: 0.5rem;
    }

    .welcome-text {
        font-size: 1.1rem;
        color: #b8bdc3;
        line-height: 1.6;
    }

    .action-card {
        background: #1a1f26;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #3d4349;
        text-align: center;
        height: 100%;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .action-card:hover {
        border-color: #52b788;
        transform: translateY(-2px);
    }

    .action-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .action-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #e8eaed;
        margin-bottom: 0.5rem;
    }

    .action-desc {
        font-size: 1rem;
        color: #b8bdc3;
        line-height: 1.5;
    }

    .info-card {
        background: #1a1f26;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #3d4349;
        margin-bottom: 1rem;
    }

    .info-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #52b788;
        margin-bottom: 0.5rem;
    }

    .info-text {
        font-size: 1rem;
        color: #e8eaed;
        line-height: 1.6;
    }

    .tip-box {
        background: rgba(82, 183, 136, 0.1);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #52b788;
        margin: 1rem 0;
    }

    .tip-text {
        font-size: 1rem;
        color: #e8eaed;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

user_name = st.session_state.get("farmer_profile", {}).get("name", "Bạn")
current_hour = datetime.now().hour

if current_hour < 12:
    greeting = "Chào buổi sáng"
elif current_hour < 18:
    greeting = "Chào buổi chiều"
else:
    greeting = "Chào buổi tối"

st.markdown(f"""
    <div class='welcome-box'>
        <div class='welcome-title'>{greeting}, {user_name}!</div>
        <div class='welcome-text'>
            Chúng tôi ở đây để giúp bạn chăm sóc ruộng đất tốt hơn.
            Hãy chọn điều bạn cần bên dưới.
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("### Bạn cần làm gì hôm nay?")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class='action-card'>
            <div class='action-icon'>💬</div>
            <div class='action-title'>Hỏi về vấn đề ruộng</div>
            <div class='action-desc'>Lúa vàng lá? Nước mặn? Hỏi ngay để được tư vấn</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Hỏi ngay", key="ask_ai", use_container_width=True, type="primary"):
        st.switch_page("pages/ai_consultation.py")

with col2:
    st.markdown("""
        <div class='action-card'>
            <div class='action-icon'>🌤️</div>
            <div class='action-title'>Xem thời tiết & độ mặn</div>
            <div class='action-desc'>Kiểm tra thời tiết và cảnh báo nước mặn</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Xem ngay", key="check_weather", use_container_width=True, type="primary"):
        st.switch_page("pages/utilities.py")

st.markdown("<br>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
        <div class='action-card'>
            <div class='action-icon'>👨‍🌾</div>
            <div class='action-title'>Gọi chuyên gia</div>
            <div class='action-desc'>Nói chuyện trực tiếp với chuyên gia nông nghiệp</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Tìm chuyên gia", key="find_expert", use_container_width=True):
        st.switch_page("pages/experts.py")

with col4:
    st.markdown("""
        <div class='action-card'>
            <div class='action-icon'>📝</div>
            <div class='action-title'>Thông tin ruộng của tôi</div>
            <div class='action-desc'>Cập nhật diện tích, loại đất, cây trồng</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Cập nhật", key="update_profile", use_container_width=True):
        st.switch_page("pages/profile.py")

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("### Mẹo hữu ích")

st.markdown("""
    <div class='tip-box'>
        <div class='tip-text'>
            💡 <strong>Mùa mưa sắp đến:</strong> Kiểm tra độ mặn trong nước thường xuyên để điều chỉnh lịch gieo trồng phù hợp.
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='tip-box'>
        <div class='tip-text'>
            💡 <strong>Lúa vàng lá?</strong> Có thể do thiếu dinh dưỡng hoặc nước mặn. Hỏi AI hoặc chuyên gia để được tư vấn cụ thể.
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='tip-box'>
        <div class='tip-text'>
            💡 <strong>Cập nhật thông tin ruộng:</strong> Giúp chúng tôi tư vấn chính xác hơn cho tình hình của bạn.
        </div>
    </div>
""", unsafe_allow_html=True)

