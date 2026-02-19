import streamlit as st
from utils.database import get_farmer_profile, save_farmer_profile

theme = st.session_state.get("theme", "light")
user_id = st.session_state.get("user_id", 1)

existing_profile = get_farmer_profile(user_id)

if theme == "light":
    st.markdown("""
    <style>
        .form-section-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2d6a4f;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #2d6a4f;
        }

        .info-banner {
            background-color: #d8f3dc;
            border-left: 4px solid #2d6a4f;
            padding: 1rem 1.5rem;
            border-radius: 6px;
            margin-bottom: 2rem;
        }

        .profile-summary {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #dee2e6;
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .form-section-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #52b788;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #52b788;
        }

        .info-banner {
            background-color: rgba(45, 106, 79, 0.15);
            border-left: 4px solid #52b788;
            padding: 1rem 1.5rem;
            border-radius: 6px;
            margin-bottom: 2rem;
            border: 1px solid #3d4349;
        }

        .profile-summary {
            background: #1a1f26;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #3d4349;
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Hồ Sơ Nông Hộ")

banner_color = "#065f46" if theme == "light" else "#a7f3d0"
st.markdown(f"""
    <div class='info-banner'>
        <p style='margin: 0; color: {banner_color};'>
            Vui lòng cung cấp thông tin về ruộng đất của bạn để nhận được tư vấn chính xác hơn.
        </p>
    </div>
""", unsafe_allow_html=True)

with st.form("farmer_profile_form"):

    st.markdown("<div class='form-section-header'>Thông tin cơ bản</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Họ và tên *",
                            value=existing_profile.get('name', '') if existing_profile else '',
                            placeholder="Nguyễn Văn A")
    with col2:
        phone = st.text_input("Số điện thoại *",
                             value=existing_profile.get('phone', '') if existing_profile else '',
                             placeholder="0912345678")

    col1, col2 = st.columns(2)
    with col1:
        provinces = ["An Giang", "Bạc Liêu", "Bến Tre", "Cà Mau", "Cần Thơ",
                    "Đồng Tháp", "Hậu Giang", "Kiên Giang", "Long An",
                    "Sóc Trăng", "Tiền Giang", "Trà Vinh", "Vĩnh Long"]
        default_province = 0
        if existing_profile and existing_profile.get('province') in provinces:
            default_province = provinces.index(existing_profile.get('province'))
        province = st.selectbox("Tỉnh/Thành phố *", provinces, index=default_province)
    with col2:
        district = st.text_input("Quận/Huyện *",
                                value=existing_profile.get('district', '') if existing_profile else '',
                                placeholder="Châu Đốc")

    st.markdown("<div class='form-section-header'>Thông tin ruộng đất</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input(
            "Diện tích (ha) *",
            min_value=0.0,
            max_value=1000.0,
            value=float(existing_profile.get('area', 0.0)) if existing_profile else 0.0,
            step=0.1,
            format="%.1f"
        )
    with col2:
        salinity = st.number_input(
            "Độ mặn (‰)",
            min_value=0.0,
            max_value=50.0,
            value=float(existing_profile.get('salinity', 0.0)) if existing_profile else 0.0,
            step=0.1,
            format="%.1f",
            help="Độ mặn của nước tưới (đơn vị: phần nghìn)"
        )

    col1, col2 = st.columns(2)
    with col1:
        soil_types = ["Phù sa", "Phù sa pha cát", "Cát", "Sét", "Phèn", "Mặn"]
        default_soil = 0
        if existing_profile and existing_profile.get('soil_type') in soil_types:
            default_soil = soil_types.index(existing_profile.get('soil_type'))
        soil_type = st.selectbox("Loại đất *", soil_types, index=default_soil)
    with col2:
        water_sources = ["Sông", "Kênh", "Mưa", "Giếng", "Ao hồ", "Khác"]
        default_water = 0
        if existing_profile and existing_profile.get('water_source') in water_sources:
            default_water = water_sources.index(existing_profile.get('water_source'))
        water_source = st.selectbox("Nguồn nước chính", water_sources, index=default_water)

    st.markdown("<div class='form-section-header'>Lịch sử canh tác</div>", unsafe_allow_html=True)

    crop_options = ["Lúa", "Tôm", "Cá", "Rau màu", "Cây ăn trái", "Hoa màu", "Khác"]
    default_crops = existing_profile.get('crops', []) if existing_profile else []
    crops = st.multiselect(
        "Cây trồng hiện tại *",
        crop_options,
        default=default_crops,
        help="Chọn tất cả các loại cây trồng/nuôi trồng trên ruộng"
    )

    production_models = ["Lúa thuần", "Lúa - Tôm", "Lúa - Cá", "Tôm thuần", "Cá thuần", "Rau màu", "Khác"]
    default_model_idx = 0
    if existing_profile and existing_profile.get('production_model') in production_models:
        default_model_idx = production_models.index(existing_profile.get('production_model'))
    production_model = st.radio(
        "Mô hình sản xuất *",
        production_models,
        index=default_model_idx,
        horizontal=True
    )

    col1, col2 = st.columns(2)
    with col1:
        seasons_per_year = st.number_input(
            "Số vụ/năm",
            min_value=1,
            max_value=4,
            value=int(existing_profile.get('seasons_per_year', 2)) if existing_profile else 2,
            step=1
        )
    with col2:
        avg_yield = st.number_input(
            "Năng suất trung bình (tấn/ha)",
            min_value=0.0,
            max_value=20.0,
            value=float(existing_profile.get('avg_yield', 0.0)) if existing_profile else 0.0,
            step=0.1,
            format="%.1f"
        )

    notes = st.text_area(
        "Ghi chú thêm",
        value=existing_profile.get('notes', '') if existing_profile else '',
        placeholder="Ví dụ: Ruộng hay bị ngập mặn vào tháng 3-4, đã từng bị bệnh đạo ôn...",
        height=100
    )

    submitted = st.form_submit_button("Lưu thông tin", use_container_width=True, type="primary")

    if submitted:
        if not name or not phone or not province or not district or area <= 0 or not soil_type or not crops or not production_model:
            st.error("Vui lòng điền đầy đủ các trường bắt buộc (đánh dấu *)")
        else:
            profile_data = {
                "name": name,
                "phone": phone,
                "province": province,
                "district": district,
                "area": area,
                "salinity": salinity,
                "soil_type": soil_type,
                "water_source": water_source,
                "crops": crops,
                "production_model": production_model,
                "seasons_per_year": seasons_per_year,
                "avg_yield": avg_yield,
                "notes": notes
            }

            try:
                save_farmer_profile(user_id, profile_data)
                st.session_state.farmer_profile = profile_data
                st.success("Đã lưu thông tin thành công!")
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi khi lưu thông tin: {str(e)}")


if existing_profile:
    st.markdown("<div class='form-section-header'>Thông tin đã lưu</div>", unsafe_allow_html=True)

    st.markdown("<div class='profile-summary'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Họ tên:** {existing_profile.get('name', 'N/A')}")
        st.write(f"**Số điện thoại:** {existing_profile.get('phone', 'N/A')}")
        st.write(f"**Địa chỉ:** {existing_profile.get('district', 'N/A')}, {existing_profile.get('province', 'N/A')}")
        st.write(f"**Diện tích:** {existing_profile.get('area', 0)} ha")
        st.write(f"**Độ mặn:** {existing_profile.get('salinity', 0)} ‰")

    with col2:
        st.write(f"**Loại đất:** {existing_profile.get('soil_type', 'N/A')}")
        st.write(f"**Nguồn nước:** {existing_profile.get('water_source', 'N/A')}")
        crops_list = existing_profile.get('crops', [])
        if isinstance(crops_list, list):
            st.write(f"**Cây trồng:** {', '.join(crops_list)}")
        else:
            st.write(f"**Cây trồng:** {crops_list}")
        st.write(f"**Mô hình:** {existing_profile.get('production_model', 'N/A')}")
        st.write(f"**Số vụ/năm:** {existing_profile.get('seasons_per_year', 0)}")

    st.markdown("</div>", unsafe_allow_html=True)

