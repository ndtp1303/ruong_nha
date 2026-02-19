import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
from utils.database import (
    get_active_consultation, create_consultation,
    save_message, get_consultation_messages,
    save_contact_request, get_all_experts,
    get_consultation_history
)

theme = st.session_state.get("theme", "light")
user_id = st.session_state.get("user_id", 1)

if theme == "light":
    st.markdown("""
    <style>
        .chat-header {
            text-align: center;
            padding: 2rem 0;
            border-bottom: 1px solid #dee2e6;
            margin-bottom: 2rem;
        }

        .chat-title {
            font-size: 2rem;
            font-weight: 600;
            color: #2d6a4f;
            margin-bottom: 0.5rem;
        }

        .chat-subtitle {
            font-size: 1rem;
            color: #495057;
        }

        .expert-recommendation {
            background: #d8f3dc;
            border-left: 4px solid #2d6a4f;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        }

        .expert-rec-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: #2d6a4f;
            margin-bottom: 0.5rem;
        }

        .contact-form {
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
        .chat-header {
            text-align: center;
            padding: 2rem 0;
            border-bottom: 1px solid #3d4349;
            margin-bottom: 2rem;
        }

        .chat-title {
            font-size: 2rem;
            font-weight: 600;
            color: #52b788;
            margin-bottom: 0.5rem;
        }

        .chat-subtitle {
            font-size: 1rem;
            color: #b8bdc3;
        }

        .expert-recommendation {
            background: rgba(45, 106, 79, 0.15);
            border-left: 4px solid #52b788;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            border: 1px solid #3d4349;
        }

        .expert-rec-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: #52b788;
            margin-bottom: 0.5rem;
        }

        .contact-form {
            background: #1a1f26;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #3d4349;
            margin-top: 1rem;
        }

        .history-item {
            background: #1a1f26;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            border: 1px solid #3d4349;
            margin-bottom: 0.75rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .history-item:hover {
            border-color: #52b788;
            transform: translateX(4px);
        }

        .history-date {
            font-size: 0.9rem;
            color: #52b788;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .history-preview {
            font-size: 1rem;
            color: #e8eaed;
            margin-bottom: 0.25rem;
        }

        .history-meta {
            font-size: 0.85rem;
            color: #b8bdc3;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class='chat-header'>
        <h1 class='chat-title'>Tư Vấn AI</h1>
        <p class='chat-subtitle'>Mô tả vấn đề bạn đang gặp phải, AI sẽ giúp phân tích và gợi ý giải pháp</p>
    </div>
""", unsafe_allow_html=True)

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "chat"

if "selected_consultation_id" not in st.session_state:
    st.session_state.selected_consultation_id = None

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "chat"

if "selected_consultation_id" not in st.session_state:
    st.session_state.selected_consultation_id = None

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("💬 Tư vấn mới", use_container_width=True, type="primary" if st.session_state.view_mode == "chat" else "secondary"):
        st.session_state.view_mode = "chat"
        st.session_state.selected_consultation_id = None
        st.rerun()

with col2:
    if st.button("📋 Lịch sử tư vấn", use_container_width=True, type="primary" if st.session_state.view_mode == "history" else "secondary"):
        st.session_state.view_mode = "history"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.view_mode == "history":
    history = get_consultation_history(user_id)

    if not history:
        st.info("Bạn chưa có lịch sử tư vấn nào.")
    else:
        st.markdown("### Các cuộc tư vấn trước đây")
        st.markdown("<br>", unsafe_allow_html=True)

        for item in history:
            consultation_id = item['id']
            created_at = datetime.fromisoformat(item['created_at']).strftime("%d/%m/%Y %H:%M")
            first_msg = item.get('first_message', 'Không có tin nhắn')
            msg_count = item.get('message_count', 0)
            status = item.get('status', 'active')

            preview = first_msg[:80] + "..." if len(first_msg) > 80 else first_msg

            st.markdown(f"""
                <div class='history-item'>
                    <div class='history-date'>📅 {created_at}</div>
                    <div class='history-preview'>{preview}</div>
                    <div class='history-meta'>{msg_count} tin nhắn • Trạng thái: {status}</div>
                </div>
            """, unsafe_allow_html=True)

            if st.button("Xem chi tiết", key=f"view_{consultation_id}", use_container_width=True):
                st.session_state.selected_consultation_id = consultation_id
                st.session_state.view_mode = "detail"
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

elif st.session_state.view_mode == "detail":
    consultation_id = st.session_state.selected_consultation_id

    if st.button("← Quay lại lịch sử", type="secondary"):
        st.session_state.view_mode = "history"
        st.session_state.selected_consultation_id = None
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Chi tiết cuộc tư vấn")
    st.markdown("<br>", unsafe_allow_html=True)

    messages = get_consultation_messages(consultation_id)

    if not messages:
        st.info("Không có tin nhắn trong cuộc tư vấn này.")
    else:
        for msg in messages:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])

else:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.warning("Chưa cấu hình API key. Vui lòng tạo file .env và thêm GEMINI_API_KEY")
        st.info("""
            **Hướng dẫn:**
            1. Sao chép file `.env.example` thành `.env`
            2. Lấy API key từ: https://makersuite.google.com/app/apikey
            3. Thêm API key vào file `.env`
        """)
        st.stop()

    genai.configure(api_key=api_key)

    @st.cache_resource
    def load_model():
        return genai.GenerativeModel('models/gemini-2.5-flash')

    model = load_model()

    SYSTEM_PROMPT = """Bạn là chuyên gia tư vấn nông nghiệp AI cho nông dân Việt Nam.
Nhiệm vụ của bạn là:
1. Phân loại vấn đề nông dân gặp phải (xâm nhập mặn, sâu bệnh, dinh dưỡng, thời tiết, thị trường)
2. Đưa ra giải pháp cụ thể, dễ hiểu, phù hợp với điều kiện Việt Nam
3. Gợi ý loại chuyên gia phù hợp để tư vấn thêm

Trả lời bằng tiếng Việt, ngắn gọn, dễ hiểu, thực tế."""

    consultation = get_active_consultation(user_id)
    if not consultation:
        consultation_id = create_consultation(user_id)
        consultation = {'id': consultation_id}
    else:
        consultation_id = consultation['id']

    if "messages_loaded" not in st.session_state:
        messages = get_consultation_messages(consultation_id)
        st.session_state.messages = [{"role": msg['role'], "content": msg['content']} for msg in messages]
        st.session_state.messages_loaded = True

    def contact_expert(expert_id, expert_name, expert_specialty):
        st.markdown(f"<div class='contact-form'>", unsafe_allow_html=True)
        st.markdown(f"### Liên hệ: {expert_name}")
        st.markdown(f"**Chuyên môn:** {expert_specialty}")

        with st.form(key=f"contact_form_{expert_id}"):
            contact_method = st.radio(
                "Phương thức liên hệ",
                ["Nhắn tin", "Video call", "Điện thoại"],
                horizontal=True
            )

            subject = st.text_input("Chủ đề", placeholder="VD: Tư vấn về xâm nhập mặn")
            message = st.text_area(
                "Nội dung",
                placeholder="Mô tả chi tiết vấn đề của bạn...",
                height=150
            )

            preferred_time = st.selectbox(
                "Thời gian mong muốn",
                ["Sáng (8h-11h)", "Chiều (14h-17h)", "Tối (19h-21h)", "Bất kỳ"]
            )

            submit = st.form_submit_button("Gửi yêu cầu", type="primary", use_container_width=True)

            if submit:
                if not subject or not message:
                    st.error("Vui lòng điền đầy đủ thông tin")
                else:
                    try:
                        save_contact_request(
                            user_id=user_id,
                            expert_id=expert_id,
                            subject=subject,
                            message=message,
                            contact_method=contact_method,
                            preferred_time=preferred_time
                        )
                        st.success(f"Đã gửi yêu cầu liên hệ đến {expert_name}!")
                    except Exception as e:
                        st.error(f"Lỗi: {str(e)}")

        st.markdown("</div>", unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Mô tả vấn đề của bạn... (VD: Nước mặn 4‰, lúa vàng lá)"):

        context = ""
        if st.session_state.farmer_profile:
            profile = st.session_state.farmer_profile
            context = f"""

            **Thông tin nông hộ:**
            - Địa điểm: {profile.get('district', '')}, {profile.get('province', '')}
            - Diện tích: {profile.get('area', 0)} ha
            - Loại đất: {profile.get('soil_type', '')}
            - Độ mặn: {profile.get('salinity', 0)} ‰
            - Cây trồng: {', '.join(profile.get('crops', []))}
            - Mô hình: {profile.get('production_model', '')}
            """

        st.session_state.messages.append({"role": "user", "content": prompt})
        save_message(consultation_id, "user", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI đang phân tích..."):
                try:
                    full_prompt = f"{SYSTEM_PROMPT}\n{context}\n\nVấn đề: {prompt}"

                    response = model.generate_content(full_prompt)
                    response_text = response.text

                    st.markdown(response_text)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text
                    })
                    save_message(consultation_id, "assistant", response_text)

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("<div class='expert-recommendation'>", unsafe_allow_html=True)
                    st.markdown("<div class='expert-rec-title'>Chuyên gia đề xuất</div>", unsafe_allow_html=True)

                    keywords = {
                        "Thủy lợi & Xâm nhập mặn": ["mặn", "xâm nhập", "nước", "tưới", "thủy lợi", "độ mặn"],
                        "Bệnh cây trồng": ["bệnh", "sâu", "vàng lá", "héo", "chết", "nấm", "vi khuẩn"],
                        "Chuyển đổi mô hình": ["chuyển đổi", "mô hình", "lúa-tôm", "lúa-cá", "canh tác"],
                        "Thị trường": ["giá", "thị trường", "bán", "tiêu thụ", "xuất khẩu"],
                        "Dinh dưỡng cây trồng": ["phân", "dinh dưỡng", "bón", "đạm", "lân", "kali"]
                    }

                    prompt_lower = prompt.lower()
                    matched_specialties = []

                    for specialty, kws in keywords.items():
                        if any(kw in prompt_lower for kw in kws):
                            matched_specialties.append(specialty)

                    if not matched_specialties:
                        matched_specialties = ["Thủy lợi & Xâm nhập mặn"]

                    experts = get_all_experts()
                    recommended_experts = [e for e in experts if e['specialty'] in matched_specialties]

                    if recommended_experts:
                        for expert in recommended_experts[:2]:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**{expert['name']}** - {expert['specialty']}")
                                st.caption(f"📍 {expert['location']} | ⭐ {expert['rating_avg']}/5")
                            with col2:
                                if st.button("Liên hệ", key=f"contact_expert_{expert['id']}"):
                                    st.session_state[f"show_contact_{expert['id']}"] = True

                            if st.session_state.get(f"show_contact_{expert['id']}", False):
                                contact_expert(expert['id'], expert['name'], expert['specialty'])
                    else:
                        st.write("Vui lòng truy cập trang Chuyên gia để xem danh sách đầy đủ")

                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Lỗi: {str(e)}")
                    st.info("Vui lòng kiểm tra lại API key hoặc kết nối internet")

    with st.sidebar:
        st.markdown("### Mẹo sử dụng")
        st.info("""
        - Mô tả vấn đề cụ thể
        - Cung cấp thông tin về ruộng đất
        - Đính kèm ảnh nếu có thể
        - Đặt câu hỏi rõ ràng
        """)

        if st.button("Xóa lịch sử chat hiện tại", use_container_width=True):
            st.session_state.messages = []
            st.session_state.messages_loaded = False
            st.rerun()
