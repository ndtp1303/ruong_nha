import streamlit as st
import os
from dotenv import load_dotenv
from utils.database import init_database, seed_experts

load_dotenv()

st.set_page_config(
    page_title="Nông Nghiệp Thông Minh",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "db_initialized" not in st.session_state:
    init_database()
    seed_experts()
    st.session_state.db_initialized = True

if "user_id" not in st.session_state:
    st.session_state.user_id = 1

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "farmer_profile" not in st.session_state:
    st.session_state.farmer_profile = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #0e1117;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #e8eaed;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: #e8eaed;
    }

    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }

    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

home_page = st.Page("pages/home.py", title="Trang Chủ", icon=":material/home:", default=True)
profile_page = st.Page("pages/profile.py", title="Hồ Sơ Nông Hộ", icon=":material/person:")
ai_page = st.Page("pages/ai_consultation.py", title="Tư Vấn AI", icon=":material/chat:")
experts_page = st.Page("pages/experts.py", title="Chuyên Gia", icon=":material/groups:")
utilities_page = st.Page("pages/utilities.py", title="Tiện Ích", icon=":material/widgets:")
expert_panel_page = st.Page("pages/expert_panel.py", title="Panel Chuyên Gia", icon=":material/admin_panel_settings:")

pg = st.navigation({
    "Chính": [home_page],
    "Dịch vụ": [ai_page, experts_page, utilities_page],
    "Chuyên gia": [expert_panel_page],
    "Tài khoản": [profile_page]
})

pg.run()
