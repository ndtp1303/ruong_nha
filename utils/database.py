import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager

DATABASE_PATH = "nghi.db"

@contextmanager
def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                phone TEXT,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farmer_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                province TEXT,
                district TEXT,
                area REAL,
                salinity REAL,
                soil_type TEXT,
                water_source TEXT,
                crops TEXT,
                production_model TEXT,
                seasons_per_year INTEGER,
                avg_yield REAL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consultation_id INTEGER,
                role TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (consultation_id) REFERENCES consultations(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                specialty TEXT,
                bio TEXT,
                experience_years INTEGER,
                location TEXT,
                price_per_session INTEGER,
                rating_avg REAL DEFAULT 0,
                total_reviews INTEGER DEFAULT 0,
                total_consultations INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                expert_id INTEGER,
                subject TEXT,
                message TEXT,
                contact_method TEXT,
                preferred_time TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                responded_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (expert_id) REFERENCES experts(id)
            )
        """)
        
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE id = 1")
        if cursor.fetchone()['count'] == 0:
            cursor.execute("""
                INSERT INTO users (id, name, email, phone) 
                VALUES (1, 'Nông dân mẫu', 'farmer@example.com', '0123456789')
            """)

def seed_experts():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM experts")
        if cursor.fetchone()['count'] == 0:
            experts_data = [
                ("Nguyễn Văn An", "nva@expert.vn", "0901234567", "Thủy lợi & Xâm nhập mặn", 
                 "Chuyên gia về quản lý nước và xâm nhập mặn tại ĐBSCL", 15, "Cần Thơ", 150000, 4.8, 127, 450),
                ("Trần Thị Bình", "ttb@expert.vn", "0902345678", "Bệnh cây trồng",
                 "Tiến sĩ bệnh học cây trồng, chuyên về lúa và cây ăn trái", 12, "An Giang", 120000, 4.9, 98, 380),
                ("Lê Minh Cường", "lmc@expert.vn", "0903456789", "Chuyển đổi mô hình",
                 "Tư vấn chuyển đổi mô hình canh tác bền vững", 10, "Sóc Trăng", 100000, 4.7, 85, 320),
                ("Phạm Thị Dung", "ptd@expert.vn", "0904567890", "Thị trường",
                 "Chuyên gia phân tích thị trường nông sản", 8, "TP.HCM", 130000, 4.6, 72, 280),
                ("Hoàng Văn Em", "hve@expert.vn", "0905678901", "Dinh dưỡng cây trồng",
                 "Kỹ sư nông nghiệp, chuyên về phân bón và dinh dưỡng", 14, "Vĩnh Long", 110000, 4.8, 103, 410),
                ("Võ Thị Phương", "vtp@expert.vn", "0906789012", "Công nghệ canh tác",
                 "Chuyên gia về ứng dụng công nghệ trong nông nghiệp", 9, "Đồng Tháp", 140000, 4.7, 91, 350)
            ]
            cursor.executemany("""
                INSERT INTO experts (name, email, phone, specialty, bio, experience_years,
                                   location, price_per_session, rating_avg, total_reviews, total_consultations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, experts_data)

def get_or_create_user(user_id=1):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return dict(user)
        return None

def save_farmer_profile(user_id, profile_data):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Cập nhật thông tin user (name, phone)
        if 'name' in profile_data or 'phone' in profile_data:
            cursor.execute("""
                UPDATE users SET
                    name = ?,
                    phone = ?
                WHERE id = ?
            """, (profile_data.get('name'), profile_data.get('phone'), user_id))

        # Lưu thông tin farmer profile
        cursor.execute("SELECT id FROM farmer_profiles WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()

        crops_json = json.dumps(profile_data.get('crops', []))

        if existing:
            cursor.execute("""
                UPDATE farmer_profiles SET
                    province = ?, district = ?, area = ?, salinity = ?,
                    soil_type = ?, water_source = ?, crops = ?,
                    production_model = ?, seasons_per_year = ?, avg_yield = ?,
                    notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (profile_data.get('province'), profile_data.get('district'),
                  profile_data.get('area'), profile_data.get('salinity'),
                  profile_data.get('soil_type'), profile_data.get('water_source'),
                  crops_json, profile_data.get('production_model'),
                  profile_data.get('seasons_per_year'), profile_data.get('avg_yield'),
                  profile_data.get('notes'), user_id))
        else:
            cursor.execute("""
                INSERT INTO farmer_profiles (user_id, province, district, area, salinity,
                    soil_type, water_source, crops, production_model, seasons_per_year,
                    avg_yield, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, profile_data.get('province'), profile_data.get('district'),
                  profile_data.get('area'), profile_data.get('salinity'),
                  profile_data.get('soil_type'), profile_data.get('water_source'),
                  crops_json, profile_data.get('production_model'),
                  profile_data.get('seasons_per_year'), profile_data.get('avg_yield'),
                  profile_data.get('notes')))

def get_farmer_profile(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Lấy thông tin từ cả users và farmer_profiles
        cursor.execute("""
            SELECT u.name, u.phone, fp.*
            FROM users u
            LEFT JOIN farmer_profiles fp ON u.id = fp.user_id
            WHERE u.id = ?
        """, (user_id,))

        profile = cursor.fetchone()
        if profile:
            profile_dict = dict(profile)
            if profile_dict.get('crops'):
                profile_dict['crops'] = json.loads(profile_dict['crops'])
            return profile_dict
        return None

def get_all_experts():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM experts WHERE is_active = 1 ORDER BY rating_avg DESC")
        return [dict(row) for row in cursor.fetchall()]

def get_expert_by_id(expert_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM experts WHERE id = ?", (expert_id,))
        expert = cursor.fetchone()
        return dict(expert) if expert else None

def save_contact_request(user_id, expert_id, subject, message, contact_method, preferred_time):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contact_requests (user_id, expert_id, subject, message,
                                         contact_method, preferred_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, expert_id, subject, message, contact_method, preferred_time))
        return cursor.lastrowid

def get_contact_requests(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cr.*, e.name as expert_name, e.specialty
            FROM contact_requests cr
            JOIN experts e ON cr.expert_id = e.id
            WHERE cr.user_id = ?
            ORDER BY cr.created_at DESC
        """, (user_id,))
        return [dict(row) for row in cursor.fetchall()]

def create_consultation(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO consultations (user_id) VALUES (?)", (user_id,))
        return cursor.lastrowid

def save_message(consultation_id, role, content):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (consultation_id, role, content)
            VALUES (?, ?, ?)
        """, (consultation_id, role, content))

def get_consultation_messages(consultation_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM messages
            WHERE consultation_id = ?
            ORDER BY timestamp ASC
        """, (consultation_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_active_consultation(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM consultations
            WHERE user_id = ? AND status = 'active'
            ORDER BY created_at DESC LIMIT 1
        """, (user_id,))
        consultation = cursor.fetchone()
        return dict(consultation) if consultation else None

def get_consultation_history(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*,
                   (SELECT content FROM messages WHERE consultation_id = c.id AND role = 'user' ORDER BY timestamp ASC LIMIT 1) as first_message,
                   (SELECT COUNT(*) FROM messages WHERE consultation_id = c.id) as message_count
            FROM consultations c
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
        """, (user_id,))
        return [dict(row) for row in cursor.fetchall()]

