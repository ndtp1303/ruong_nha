#!/bin/bash

# Script để chạy ứng dụng Nông Nghiệp Thông Minh

echo "🌾 Khởi động Nông Nghiệp Thông Minh..."
echo ""

# Kiểm tra file .env
if [ ! -f .env ]; then
    echo "⚠️  Chưa có file .env"
    echo "📝 Đang tạo file .env từ .env.example..."
    cp .env.example .env
    echo "✅ Đã tạo file .env"
    echo ""
    echo "⚠️  QUAN TRỌNG: Vui lòng chỉnh sửa file .env và thêm GEMINI_API_KEY của bạn"
    echo "   Lấy API key miễn phí tại: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Nhấn Enter sau khi đã cập nhật API key..."
fi

# Kiểm tra virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Tạo virtual environment..."
    python3 -m venv venv
fi

# Kích hoạt virtual environment
echo "🔧 Kích hoạt virtual environment..."
source venv/bin/activate

# Cài đặt dependencies
echo "📥 Cài đặt dependencies..."
pip install -q -r requirements.txt

# Chạy ứng dụng
echo ""
echo "🚀 Khởi động ứng dụng..."
echo "📱 Ứng dụng sẽ mở tại: http://localhost:8501"
echo ""
streamlit run app.py

