import streamlit as st
from datetime import datetime
from utils.database import get_all_experts, save_contact_request, get_contact_requests

theme = st.session_state.get("theme", "light")
user_id = st.session_state.get("user_id", 1)

if theme == "light":
    st.markdown("""
    <style>
        .expert-header {
            text-align: center;
            padding: 2rem 0;
            border-bottom: 1px solid #dee2e6;
            margin-bottom: 2rem;
        }

        .expert-title {
            font-size: 2rem;
            font-weight: 600;
            color: #2d6a4f;
            margin-bottom: 0.5rem;
        }

        .expert-subtitle {
            font-size: 1rem;
            color: #495057;
        }

        .expert-card {
            background: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 12px;
            padding: 1.5rem;
            height: 100%;
            transition: all 0.2s ease;
        }

        .expert-card:hover {
            border-color: #2d6a4f;
            box-shadow: 0 4px 12px rgba(45, 106, 79, 0.1);
            transform: translateY(-2px);
        }

        .expert-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #2d6a4f;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            font-weight: 600;
            margin: 0 auto 1rem;
        }

        .expert-name {
            font-size: 1.25rem;
            font-weight: 600;
            color: #212529;
            text-align: center;
            margin-bottom: 0.5rem;
        }

        .expert-specialty {
            color: #2d6a4f;
            font-weight: 500;
            text-align: center;
            margin-bottom: 0.75rem;
        }

        .expert-stats {
            display: flex;
            justify-content: space-around;
            padding: 0.75rem 0;
            border-top: 1px solid #dee2e6;
            border-bottom: 1px solid #dee2e6;
            margin: 1rem 0;
        }

        .stat-item {
            text-align: center;
        }

        .stat-value {
            font-weight: 600;
            color: #212529;
        }

        .stat-label {
            font-size: 0.875rem;
            color: #6c757d;
        }

        .contact-form-modal {
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
        .expert-header {
            text-align: center;
            padding: 2rem 0;
            border-bottom: 1px solid #3d4349;
            margin-bottom: 2rem;
        }

        .expert-title {
            font-size: 2rem;
            font-weight: 600;
            color: #52b788;
            margin-bottom: 0.5rem;
        }

        .expert-subtitle {
            font-size: 1rem;
            color: #b8bdc3;
        }

        .expert-card {
            background: #1a1f26;
            border: 1px solid #3d4349;
            border-radius: 12px;
            padding: 1.5rem;
            height: 100%;
            transition: all 0.2s ease;
        }

        .expert-card:hover {
            border-color: #52b788;
            box-shadow: 0 0 0 1px #52b788;
            transform: translateY(-2px);
        }

        .expert-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #52b788;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            font-weight: 600;
            margin: 0 auto 1rem;
        }

        .expert-name {
            font-size: 1.25rem;
            font-weight: 600;
            color: #e8eaed;
            text-align: center;
            margin-bottom: 0.5rem;
        }

        .expert-specialty {
            color: #52b788;
            font-weight: 500;
            text-align: center;
            margin-bottom: 0.75rem;
        }

        .expert-stats {
            display: flex;
            justify-content: space-around;
            padding: 0.75rem 0;
            border-top: 1px solid #3d4349;
            border-bottom: 1px solid #3d4349;
            margin: 1rem 0;
        }

        .stat-item {
            text-align: center;
        }

        .stat-value {
            font-weight: 600;
            color: #e8eaed;
        }

        .stat-label {
            font-size: 0.875rem;
            color: #8a9199;
        }

        .contact-form-modal {
            background: #1a1f26;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #3d4349;
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class='expert-header'>
        <h1 class='expert-title'>Danh Sách Chuyên Gia</h1>
        <p class='expert-subtitle'>Kết nối với các chuyên gia nông nghiệp hàng đầu</p>
    </div>
""", unsafe_allow_html=True)

experts_data = get_all_experts()

specialties = ["Tất cả"] + sorted(list(set([e['specialty'] for e in experts_data])))

specialty_filter = st.pills(
    "Lọc theo chuyên môn:",
    specialties,
    selection_mode="single",
    default="Tất cả"
)

st.markdown("<br>", unsafe_allow_html=True)

filtered_experts = experts_data
if specialty_filter != "Tất cả":
    filtered_experts = [e for e in experts_data if e['specialty'] == specialty_filter]

def get_initials(name):
    parts = name.split()
    if len(parts) >= 2:
        return parts[-2][0] + parts[-1][0]
    return name[0] if name else "?"

cols = st.columns(3)
for idx, expert in enumerate(filtered_experts):
    with cols[idx % 3]:
        initials = get_initials(expert['name'])

        st.markdown(f"""
            <div class='expert-card'>
                <div class='expert-avatar'>{initials}</div>
                <div class='expert-name'>{expert['name']}</div>
                <div class='expert-specialty'>{expert['specialty']}</div>
                <div class='expert-stats'>
                    <div class='stat-item'>
                        <div class='stat-value'>{expert['rating_avg']}</div>
                        <div class='stat-label'>Đánh giá</div>
                    </div>
                    <div class='stat-item'>
                        <div class='stat-value'>{expert['total_reviews']}</div>
                        <div class='stat-label'>Nhận xét</div>
                    </div>
                    <div class='stat-item'>
                        <div class='stat-value'>{expert['experience_years']}</div>
                        <div class='stat-label'>Năm KN</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.caption(f"📍 {expert['location']}")
        st.caption(expert['bio'])
        st.caption(f"💰 {expert['price_per_session']:,} VNĐ/buổi")

        if st.button("Liên hệ chuyên gia", key=f"contact_{expert['id']}", use_container_width=True, type="primary"):
            st.session_state.selected_expert = expert
            st.session_state.show_contact_form = True
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.get("show_contact_form") and st.session_state.get("selected_expert"):
    expert = st.session_state.selected_expert

    st.markdown("---")
    st.markdown(f"## Liên hệ với {expert['name']}")

    col_info, col_form = st.columns([1, 2])

    with col_info:
        st.markdown(f"""
        **Chuyên môn:** {expert['specialty']}

        **Địa điểm:** {expert['location']}

        **Kinh nghiệm:** {expert['experience_years']} năm

        **Đánh giá:** {expert['rating_avg']}/5

        **Giá:** {expert['price_per_session']:,} VNĐ/buổi
        """)

    with col_form:
        with st.form(key="contact_form", clear_on_submit=True):
            st.markdown("### Điền thông tin liên hệ")

            subject = st.text_input(
                "Chủ đề cần tư vấn",
                placeholder="VD: Tư vấn về xâm nhập mặn"
            )

            message = st.text_area(
                "Mô tả vấn đề của bạn",
                placeholder="Hãy mô tả chi tiết vấn đề bạn đang gặp phải...",
                height=150
            )

            contact_method = st.radio(
                "Hình thức liên hệ:",
                ["Điện thoại", "Nhắn tin", "Video call"],
                horizontal=True
            )

            preferred_time = st.selectbox(
                "Thời gian mong muốn:",
                ["Sáng (8h-11h)", "Chiều (14h-17h)", "Tối (19h-21h)", "Bất kỳ"]
            )

            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Gửi yêu cầu", type="primary", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("Hủy", use_container_width=True)

            if cancel:
                st.session_state.show_contact_form = False
                st.session_state.selected_expert = None
                st.rerun()

            if submit:
                if not subject or not message:
                    st.error("Vui lòng điền đầy đủ thông tin")
                else:
                    try:
                        save_contact_request(
                            user_id=user_id,
                            expert_id=expert['id'],
                            subject=subject,
                            message=message,
                            contact_method=contact_method,
                            preferred_time=preferred_time
                        )
                        st.success(f"Đã gửi yêu cầu liên hệ đến {expert['name']}!")
                        st.info("Chuyên gia sẽ liên hệ lại với bạn trong thời gian sớm nhất.")
                        st.session_state.show_contact_form = False
                        st.session_state.selected_expert = None
                    except Exception as e:
                        st.error(f"Lỗi: {str(e)}")

with st.sidebar:
    st.markdown("### Lịch sử yêu cầu")
    contact_requests = get_contact_requests(user_id)

    if contact_requests:
        for req in contact_requests[:5]:
            status_emoji = "⏳" if req['status'] == 'pending' else "✅"
            st.caption(f"{status_emoji} {req['expert_name']}")
            st.caption(f"   {req['subject']}")
            st.caption(f"   {req['created_at'][:10]}")
            st.divider()
    else:
        st.info("Chưa có yêu cầu nào")

    st.markdown("### Mẹo tư vấn")
    st.info("""
    - Chuẩn bị thông tin chi tiết về vấn đề
    - Chụp ảnh ruộng/cây trồng nếu có
    - Ghi rõ diện tích và vị trí
    - Đặt câu hỏi cụ thể
    """)


