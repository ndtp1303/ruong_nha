import streamlit as st
from utils.database import get_connection
from datetime import datetime

st.markdown("""
<style>
    .expert-panel-header {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 1px solid #3d4349;
        margin-bottom: 2rem;
    }

    .panel-title {
        font-size: 2rem;
        font-weight: 600;
        color: #52b788;
        margin-bottom: 0.5rem;
    }

    .request-card {
        background: #1a1f26;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #3d4349;
        margin-bottom: 1rem;
    }

    .request-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .request-subject {
        font-size: 1.2rem;
        font-weight: 600;
        color: #52b788;
    }

    .request-status {
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .status-pending {
        background: rgba(255, 193, 7, 0.2);
        color: #ffc107;
    }

    .status-accepted {
        background: rgba(82, 183, 136, 0.2);
        color: #52b788;
    }

    .status-completed {
        background: rgba(108, 117, 125, 0.2);
        color: #6c757d;
    }

    .request-info {
        color: #b8bdc3;
        font-size: 0.95rem;
        margin: 0.5rem 0;
    }

    .request-message {
        background: rgba(82, 183, 136, 0.1);
        padding: 1rem;
        border-radius: 6px;
        border-left: 3px solid #52b788;
        margin: 1rem 0;
        color: #e8eaed;
    }

    .stat-box {
        background: #1a1f26;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #3d4349;
        text-align: center;
    }

    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #52b788;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        font-size: 1rem;
        color: #b8bdc3;
    }
</style>
""", unsafe_allow_html=True)

if "expert_id" not in st.session_state:
    st.session_state.expert_id = None

if not st.session_state.expert_id:
    st.markdown("""
        <div class='expert-panel-header'>
            <h1 class='panel-title'>Đăng nhập Chuyên gia</h1>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("expert_login"):
        email = st.text_input("Email", placeholder="expert@example.com")
        password = st.text_input("Mật khẩu", type="password")
        submit = st.form_submit_button("Đăng nhập", use_container_width=True, type="primary")
        
        if submit:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM experts WHERE email = ?", (email,))
                expert = cursor.fetchone()
                
                if expert:
                    st.session_state.expert_id = expert['id']
                    st.session_state.expert_name = expert['name']
                    st.success(f"Chào mừng {expert['name']}!")
                    st.rerun()
                else:
                    st.error("Email hoặc mật khẩu không đúng")
    
    st.info("Demo: Dùng email của bất kỳ chuyên gia nào trong database")
    st.stop()

expert_id = st.session_state.expert_id
expert_name = st.session_state.expert_name

st.markdown(f"""
    <div class='expert-panel-header'>
        <h1 class='panel-title'>Panel Chuyên gia</h1>
        <p style='color: #b8bdc3;'>Xin chào, {expert_name}</p>
    </div>
""", unsafe_allow_html=True)

if st.button("Đăng xuất", type="secondary"):
    st.session_state.expert_id = None
    st.session_state.expert_name = None
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

with get_connection() as conn:
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) as total FROM contact_requests WHERE expert_id = ?
    """, (expert_id,))
    total_requests = cursor.fetchone()['total']
    
    cursor.execute("""
        SELECT COUNT(*) as pending FROM contact_requests 
        WHERE expert_id = ? AND status = 'pending'
    """, (expert_id,))
    pending_requests = cursor.fetchone()['pending']
    
    cursor.execute("""
        SELECT COUNT(*) as accepted FROM contact_requests 
        WHERE expert_id = ? AND status = 'accepted'
    """, (expert_id,))
    accepted_requests = cursor.fetchone()['accepted']

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-value'>{total_requests}</div>
            <div class='stat-label'>Tổng yêu cầu</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-value'>{pending_requests}</div>
            <div class='stat-label'>Chờ xử lý</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-value'>{accepted_requests}</div>
            <div class='stat-label'>Đang tư vấn</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📬 Yêu cầu mới", "✅ Đang tư vấn"])

with tab1:
    st.markdown("### Yêu cầu liên hệ mới")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cr.*, u.name as user_name, u.phone as user_phone
            FROM contact_requests cr
            JOIN users u ON cr.user_id = u.id
            WHERE cr.expert_id = ? AND cr.status = 'pending'
            ORDER BY cr.created_at DESC
        """, (expert_id,))
        pending = cursor.fetchall()
    
    if not pending:
        st.info("Không có yêu cầu mới")
    else:
        for req in pending:
            st.markdown(f"""
                <div class='request-card'>
                    <div class='request-header'>
                        <div class='request-subject'>{req['subject']}</div>
                        <div class='request-status status-pending'>Chờ xử lý</div>
                    </div>
                    <div class='request-info'>
                        👤 Nông dân: {req['user_name']}<br>
                        📞 SĐT: {req['user_phone']}<br>
                        📅 Thời gian: {req['created_at'][:16]}<br>
                        💬 Hình thức: {req['contact_method']}<br>
                        ⏰ Thời gian mong muốn: {req['preferred_time']}
                    </div>
                    <div class='request-message'>
                        {req['message']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Chấp nhận", key=f"accept_{req['id']}", use_container_width=True, type="primary"):
                    with get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE contact_requests 
                            SET status = 'accepted' 
                            WHERE id = ?
                        """, (req['id'],))
                    st.success("Đã chấp nhận yêu cầu!")
                    st.rerun()
            
            with col2:
                if st.button("❌ Từ chối", key=f"reject_{req['id']}", use_container_width=True):
                    with get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE contact_requests 
                            SET status = 'rejected' 
                            WHERE id = ?
                        """, (req['id'],))
                    st.info("Đã từ chối yêu cầu")
                    st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)

with tab2:
    st.markdown("### Các yêu cầu đang tư vấn")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cr.*, u.name as user_name, u.phone as user_phone
            FROM contact_requests cr
            JOIN users u ON cr.user_id = u.id
            WHERE cr.expert_id = ? AND cr.status = 'accepted'
            ORDER BY cr.created_at DESC
        """, (expert_id,))
        accepted = cursor.fetchall()
    
    if not accepted:
        st.info("Không có yêu cầu đang tư vấn")
    else:
        for req in accepted:
            st.markdown(f"""
                <div class='request-card'>
                    <div class='request-header'>
                        <div class='request-subject'>{req['subject']}</div>
                        <div class='request-status status-accepted'>Đang tư vấn</div>
                    </div>
                    <div class='request-info'>
                        👤 Nông dân: {req['user_name']}<br>
                        📞 SĐT: {req['user_phone']}<br>
                        💬 Hình thức: {req['contact_method']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("✅ Hoàn thành", key=f"complete_{req['id']}", use_container_width=True):
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE contact_requests 
                        SET status = 'completed' 
                        WHERE id = ?
                    """, (req['id'],))
                st.success("Đã đánh dấu hoàn thành!")
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)

