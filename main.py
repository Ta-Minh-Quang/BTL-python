from flask import Flask, request, jsonify
from mysql.connector import Error
import pandas as pd
import numpy as np
from connectdb import create_connection
import json

app = Flask(__name__)

def get_cars_dataframe():
    conn = create_connection()
    if conn is None:
        return None
    try:
        query = "SELECT * FROM car"
        df = pd.read_sql(query, conn)
        return df
    except Error as e:
        print(f"Lỗi đọc dữ liệu: {e}")
        return None
    finally:
        conn.close()

def convert_dataframe_to_dict(df):
    """Chuyển DataFrame thành list of dictionaries với cấu trúc phù hợp"""
    cars_list = []
    for _, row in df.iterrows():
        # Xử lý features (chuyển từ string về list)
        features_str = row.get('features', '')
        if features_str and isinstance(features_str, str):
            features = [f.strip() for f in features_str.split(',')]
        else:
            features = []
        
        # Xử lý technical (chuyển từ string về dict)
        technical_str = row.get('technical', '')
        technical = {}
        if technical_str and isinstance(technical_str, str):
            try:
                # Thay thế dấu ' thành " để parse JSON
                technical_str = technical_str.replace("'", "\"")
                technical = json.loads(technical_str)
            except:
                # Fallback: xử lý thủ công nếu không parse được JSON
                technical = {'power': 'N/A', 'torque': 'N/A', 'consumption': 'N/A', 'warranty': 'N/A'}
        
        car_dict = {
            'id': row['id'],
            'brand': row['brand'],
            'model': row['model'],
            'year': row['year'],
            'price': row['price'],
            'fuel': row['fuel_type'],  # Đổi tên để phù hợp với template
            'engine': row['engine_volume'],  # Đổi tên để phù hợp với template
            'transmission': row['transmission'],
            'color': row['color'],
            'seats': row['seats'],
            'description': row['description'],
            'features': features,
            'technical': technical
        }
        cars_list.append(car_dict)
    
    return cars_list

# Lấy dữ liệu từ database
df = get_cars_dataframe()
if df is not None:
    print(f"📊 Loaded {len(df)} cars from MySQL")
    print(df.head())
    # Chuyển DataFrame thành list of dictionaries
    cars = convert_dataframe_to_dict(df)
else:
    print("❌ Không thể kết nối database")
    cars = []

@app.route('/')
def home():
    if not cars:
        return "Không có dữ liệu xe", 500
    
    brands = sorted(set(car['brand'] for car in cars))
    brand_options = ''.join([f'<option value="{b}">{b}</option>' for b in brands])
    
    # Chuyển cars thành JSON string an toàn cho JavaScript
    cars_json = json.dumps(cars, ensure_ascii=False)

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hệ Thống Tra Cứu Xe Hơi</title>
        <meta charset="UTF-8">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            .header {{
                text-align: center;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }}
            h1 {{
                color: #333;
                font-size: 36px;
                margin-bottom: 10px;
            }}
            .instruction {{
                color: #666;
                font-size: 18px;
                margin-top: 10px;
            }}
            .main-content {{
                display: grid;
                grid-template-columns: 300px 1fr;
                gap: 30px;
            }}
            .filters-section {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            .results-section {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            .car-card {{
                border: 2px solid #e1e5e9;
                border-radius: 10px;
                padding: 20px;
                background: #f8f9fa;
                transition: all 0.3s ease;
                cursor: pointer;
                margin-bottom: 15px;
            }}
            .car-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                border-color: #007bff;
                background: #e3f2fd;
            }}
            .car-header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 15px;
            }}
            .car-brand {{
                font-size: 20px;
                font-weight: bold;
                color: #333;
            }}
            .car-year {{
                background: blue;
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
            }}
            .car-model {{
                font-size: 18px;
                color: #666;
                margin-bottom: 10px;
            }}
            .car-price {{
                font-size: 22px;
                font-weight: bold;
                color: #28a745;
                margin-bottom: 15px;
            }}
            .car-details {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                font-size: 14px;
                margin-bottom: 10px;
            }}
            .click-hint {{
                text-align: center;
                color: #007bff;
                font-weight: bold;
                margin-top: 10px;
                font-size: 14px;
                background: #e3f2fd;
                padding: 8px;
                border-radius: 5px;
            }}
            button {{
                background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                color: white;
                padding: 15px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                width: 100%;
                margin-top: 10px;
            }}
            .detail-info {{
                background: #e8f5e8;
                padding: 8px 12px;
                border-radius: 5px;
                margin-top: 10px;
                font-size: 13px;
                color: #2e7d32;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚗 HỆ THỐNG TRA CỨU XE HƠI</h1>
                <p class="instruction">💡 <strong>TRANG CHỦ - THÔNG TIN CƠ BẢN</strong></p>
                <p class="instruction">👉 Ấn vào từng xe để xem <strong>THÔNG TIN CHI TIẾT</strong> đầy đủ</p>
            </div>

            <div class="main-content">
                <div class="filters-section">
                    <h2>🔍 TÌM KIẾM</h2>
                    <div style="margin: 20px 0;">
                        <label for="brand">Hãng xe:</label>
                        <select id="brand" style="width: 100%; padding: 10px; margin: 5px 0;">
                            <option value="">Tất cả hãng xe</option>
                            {brand_options}
                        </select>
                    </div>
                    <button onclick="searchCars()">🔍 TÌM KIẾM</button>

                    <div class="detail-info">
                        <strong>ℹ️ Lưu ý:</strong><br>
                        • Trang này hiển thị thông tin cơ bản<br>
                        • Ấn vào xe để xem chi tiết đầy đủ
                    </div>
                </div>

                <div class="results-section">
                    <h2>📊 DANH SÁCH XE</h2>
                    <div id="carResults">
                        <!-- Kết quả sẽ hiển thị ở đây -->
                    </div>
                </div>
            </div>
        </div>

        <script>
            const allCars = {cars_json};

            document.addEventListener('DOMContentLoaded', function() {{
                displayCars(allCars);
            }});

            function displayCars(carList) {{
                const resultsDiv = document.getElementById('carResults');

                if (carList.length === 0) {{
                    resultsDiv.innerHTML = '<p>Không tìm thấy xe nào phù hợp</p>';
                    return;
                }}

                resultsDiv.innerHTML = carList.map(car => {{
                    return `
                        <div class="car-card" onclick="viewCarDetail(${{car.id}})">
                            <div class="car-header">
                                <div class="car-brand">${{car.brand}}</div>
                                <div class="car-year">${{car.year}}</div>
                            </div>
                            <div class="car-model">${{car.model}}</div>
                            <div class="car-price">${{car.price.toLocaleString()}} VND</div>
                            <div class="car-details">
                                <div>⚙️ ${{car.engine}}</div>
                                <div>⛽ ${{car.fuel}}</div>
                                <div>🔧 ${{car.transmission}}</div>
                                <div>👥 ${{car.seats}} chỗ</div>
                            </div>
                            <div class="click-hint">
                                👉 CLICK ĐỂ XEM THÔNG TIN CHI TIẾT ĐẦY ĐỦ
                            </div>
                        </div>
                    `;
                }}).join('');
            }}

            function searchCars() {{
                const brand = document.getElementById('brand').value;

                const filteredCars = allCars.filter(car => {{
                    if (brand && car.brand !== brand) return false;
                    return true;
                }});

                displayCars(filteredCars);
            }}

            function viewCarDetail(carId) {{
                window.location.href = '/car/' + carId;
            }}
        </script>
    </body>
    </html>
    '''

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = next((car for car in cars if car['id'] == car_id), None)
    if not car:
        return "Xe không tồn tại", 404

    # Tạo HTML cho features
    features_html = ''.join([f'<li>✅ {feature}</li>' for feature in car['features']])

    # Tạo HTML cho technical specs
    technical_html = f'''
        <tr><td>Công suất</td><td><strong>{car['technical'].get('power', 'N/A')}</strong></td></tr>
        <tr><td>Mô-men xoắn</td><td><strong>{car['technical'].get('torque', 'N/A')}</strong></td></tr>
        <tr><td>Mức tiêu thụ</td><td><strong>{car['technical'].get('consumption', 'N/A')}</strong></td></tr>
        <tr><td>Bảo hành</td><td><strong>{car['technical'].get('warranty', 'N/A')}</strong></td></tr>
    '''

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chi tiết {car['brand']} {car['model']}</title>
        <meta charset="UTF-8">
        <style>
            /* CSS giữ nguyên như trước */
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
            }}
            .back-button {{
                background: blue;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                margin-bottom: 20px;
                text-decoration: none;
                display: inline-block;
            }}
            .back-button:hover {{
                background: #5a6268;
            }}
            .car-detail-card {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            .car-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                border-bottom: 2px solid #e9ecef;
                padding-bottom: 20px;
            }}
            .car-title {{
                font-size: 32px;
                font-weight: bold;
                color: #333;
            }}
            .car-price {{
                font-size: 28px;
                font-weight: bold;
                color: #28a745;
                margin: 15px 0;
            }}
            .car-year {{
                background: #007bff;
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }}
            .info-section {{
                margin: 25px 0;
            }}
            .section-title {{
                font-size: 22px;
                font-weight: bold;
                color: #333;
                margin-bottom: 15px;
                border-left: 4px solid #007bff;
                padding-left: 10px;
            }}
            .basic-info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }}
            .info-item {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }}
            .info-label {{
                font-size: 12px;
                color: #666;
                text-transform: uppercase;
                font-weight: 600;
                margin-bottom: 5px;
            }}
            .info-value {{
                font-size: 16px;
                font-weight: 600;
                color: #333;
            }}
            .description-box {{
                background: #e3f2fd;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                line-height: 1.6;
            }}
            .features-list {{
                background: #f3e5f5;
                padding: 20px;
                border-radius: 10px;
                margin: 15px 0;
            }}
            .features-list ul {{
                list-style: none;
                padding: 0;
            }}
            .features-list li {{
                padding: 5px 0;
                font-size: 15px;
            }}
            .technical-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                background: #e8f5e8;
                border-radius: 10px;
                overflow: hidden;
            }}
            .technical-table td {{
                padding: 12px 15px;
                border-bottom: 1px solid #c8e6c9;
            }}
            .technical-table tr:last-child td {{
                border-bottom: none;
            }}
            .page-title {{
                text-align: center;
                color: white;
                margin-bottom: 15px;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="page-title">
                <strong>TRANG CHI TIẾT - THÔNG TIN ĐẦY ĐỦ</strong>
            </div>
            <a href="/" class="back-button"><b>← Quay lại trang chủ</b></a>

            <div class="car-detail-card">
                <div class="car-header">
                    <h1 class="car-title">{car['brand']} {car['model']}</h1>
                    <div class="car-year">{car['year']}</div>
                </div>

                <div class="car-price">{car['price']:,.0f} VND</div>

                <div class="basic-info-grid">
                    <div class="info-item">
                        <div class="info-label">Động cơ</div>
                        <div class="info-value">⚙️ {car['engine']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Nhiên liệu</div>
                        <div class="info-value">⛽ {car['fuel']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Hộp số</div>
                        <div class="info-value">🔧 {car['transmission']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Số chỗ</div>
                        <div class="info-value">👥 {car['seats']} chỗ</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Màu sắc</div>
                        <div class="info-value">🎨 {car['color']}</div>
                    </div>
                </div>

                <div class="info-section">
                    <div class="section-title">📝 MÔ TẢ CHI TIẾT</div>
                    <div class="description-box">
                        {car['description']}
                    </div>
                </div>

                <div class="info-section">
                    <div class="section-title">⭐ TÍNH NĂNG NỔI BẬT</div>
                    <div class="features-list">
                        <ul>
                            {features_html}
                        </ul>
                    </div>
                </div>

                <div class="info-section">
                    <div class="section-title">🔧 THÔNG SỐ KỸ THUẬT</div>
                    <table class="technical-table">
                        {technical_html}
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚗 KHỞI ĐỘNG HỆ THỐNG TRA CỨU XE HƠI")
    print(f"📊 Tổng số xe: {len(cars)}")
    print("🌐 Truy cập: http://localhost:5000")
    print("👉 TRANG CHỦ: Thông tin cơ bản")
    print("👉 TRANG CHI TIẾT: Ấn vào từng xe để xem thông tin đầy đủ")
    app.run(debug=True, port=5000)