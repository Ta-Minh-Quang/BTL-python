import mysql.connector
from mysql.connector import Error

def create_database():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456"
    )

    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS car_database")

def create_connection():
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = "123456",
            database = 'car_database'
        )
        if connection.is_connected():
            print("Kết nối thành công")
            return connection
    except Error as e:
        print(f"Lỗi kết nối {e}")
        return None
    
def create_table():
    conn = create_connection()

    if conn is None:
        return
    
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS car (
            id INT AUTO_INCREMENT PRIMARY KEY,
            brand VARCHAR(50) NOT NULL,
            model VARCHAR(100) NOT NULL,
            year INT,
            engine_volume VARCHAR(20),
            fuel_type VARCHAR(20),
            transmission VARCHAR(20),
            price BIGINT,
            color VARCHAR(30),
            seats INT,
            description TEXT,
            features TEXT,
            technical TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    print("Đã tạo bảng thành công")

    cursor.close()
    conn.close()

def insert_sample_data():
    conn = create_connection()

    if conn is None:
        return
    
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM car")
    count = cursor.fetchone()[0]

    if count == 0:
        cars = [
            # FORD
            {'id': 1, 'brand': 'Ford', 'model': 'Ranger', 'year': 2023, 'price': 720000000, 'fuel_type': 'Dầu', 'engine_volume': '2.0L',
             'transmission': 'Số tự động', 'color': 'Trắng', 'seats': 5,
             'description': 'Bán tải thông dụng nhất Việt Nam, mạnh mẽ, đa dụng. Động cơ Bi-Turbo công nghệ mới.',
             'features': ['Camera 360', 'Cảm biến áp suất lốp', 'Điều hòa tự động 2 vùng', 'Màn hình cảm ứng 12 inch', 'Apple CarPlay'],
             'technical': {'power': '210 mã lực', 'torque': '500 Nm', 'consumption': '7.9L/100km', 'warranty': '3 năm'}},

            {'id': 2, 'brand': 'Ford', 'model': 'Everest', 'year': 2023, 'price': 1250000000, 'fuel_type': 'Dầu', 'engine_volume': '2.0L',
             'transmission': 'Số tự động', 'color': 'Đen', 'seats': 7,
             'description': 'SUV 7 chỗ cao cấp, thiết kế thể thao. Không gian rộng rãi, công nghệ tiên tiến.',
             'features': ['Cửa sổ trời', 'Ghế da cao cấp', 'Hệ thống âm thanh B&O', 'Định vị GPS', 'Sạc không dây'],
             'technical': {'power': '180 mã lực', 'torque': '420 Nm', 'consumption': '8.3L/100km', 'warranty': '5 năm'}},

            # TOYOTA
            {'id': 3, 'brand': 'Toyota', 'model': 'Vios', 'year': 2023, 'price': 520000000, 'fuel_type': 'Xăng', 'engine_volume': '1.5L',
             'transmission': 'CVT', 'color': 'Trắng', 'seats': 5,
             'description': 'Sedan hạng B bán chạy nhất Việt Nam. Tiết kiệm nhiên liệu, vận hành êm ái, chi phí bảo trì thấp.',
             'features': ['Camera lùi', 'Cảm biến lùi', 'Điều hòa tự động', 'Màn hình cảm ứng 9 inch', 'Camera hành trình'],
             'technical': {'power': '107 mã lực', 'torque': '140 Nm', 'consumption': '5.7L/100km', 'warranty': '3 năm'}},

            {'id': 4, 'brand': 'Toyota', 'model': 'Corolla Cross', 'year': 2023, 'price': 720000000, 'fuel_type': 'Xăng', 'engine_volume': '1.8L',
             'transmission': 'CVT', 'color': 'Xám', 'seats': 5,
             'description': 'SUV hạng C cực kỳ phổ biến. Thiết kế trẻ trung, không gian rộng rãi, vận hành tiết kiệm.',
             'features': ['Camera 360', 'Cảnh báo điểm mù', 'Phanh khẩn cấp', 'Màn hình 10.1 inch', '2 cổng sạc USB'],
             'technical': {'power': '140 mã lực', 'torque': '177 Nm', 'consumption': '6.2L/100km', 'warranty': '3 năm'}},

            {'id': 5, 'brand': 'Toyota', 'model': 'Innova', 'year': 2023, 'price': 920000000, 'fuel_type': 'Xăng', 'engine_volume': '2.0L',
             'transmission': 'Số tự động', 'color': 'Bạc', 'seats': 7,
             'description': 'MPV đa dụng, phù hợp gia đình và kinh doanh. Không gian rộng rãi, động cơ bền bỉ.',
             'features': ['Camera lùi', 'Cửa hít', 'Điều hòa tự động 2 vùng', 'Màn hình 8 inch', 'Kết nối Android Auto'],
             'technical': {'power': '174 mã lực', 'torque': '205 Nm', 'consumption': '7.6L/100km', 'warranty': '3 năm'}},

            # HONDA
            {'id': 6, 'brand': 'Honda', 'model': 'City', 'year': 2023, 'price': 580000000, 'fuel_type': 'Xăng', 'engine_volume': '1.5L',
             'transmission': 'CVT', 'color': 'Đỏ', 'seats': 5,
             'description': 'Sedan hạng B với thiết kế thể thao, động cơ i-VTEC mạnh mẽ, tiết kiệm nhiên liệu.',
             'features': ['Camera lùi', 'Led tự động', 'Điều hòa tự động', 'Màn hình 8 inch', 'Lazada âm thanh 8 loa'],
             'technical': {'power': '121 mã lực', 'torque': '145 Nm', 'consumption': '5.8L/100km', 'warranty': '3 năm'}},

            {'id': 7, 'brand': 'Honda', 'model': 'CR-V', 'year': 2023, 'price': 980000000, 'fuel_type': 'Xăng', 'engine_volume': '1.5L',
             'transmission': 'CVT', 'color': 'Trắng', 'seats': 5,
             'description': 'SUV hạng C cao cấp với công nghệ an toàn tiên tiến Honda Sensing, không gian thoải mái.',
             'features': ['Honda Sensing', 'Camera 360', 'Cửa hít', 'Màn hình 9 inch', 'Sạc không dây'],
             'technical': {'power': '188 mã lực', 'torque': '243 Nm', 'consumption': '6.7L/100km', 'warranty': '3 năm'}},

            # HYUNDAI
            {'id': 8, 'brand': 'Hyundai', 'model': 'Accent', 'year': 2023, 'price': 480000000, 'fuel_type': 'Xăng', 'engine_volume': '1.4L',
             'transmission': 'CVT', 'color': 'Bạc', 'seats': 5,
             'description': 'Sedan hạng B giá tốt, thiết kế hiện đại, trang bị đầy đủ tính năng an toàn.',
             'features': ['Camera lùi', 'Cảm biến lùi', 'Điều hòa tự động', 'Màn hình 8 inch', 'Cửa sổ trời'],
             'technical': {'power': '100 mã lực', 'torque': '136 Nm', 'consumption': '5.5L/100km', 'warranty': '3 năm'}},

            {'id': 9, 'brand': 'Hyundai', 'model': 'Creta', 'year': 2023, 'price': 620000000, 'fuel_type': 'Xăng', 'engine_volume': '1.5L',
             'transmission': 'CVT', 'color': 'Xanh', 'seats': 5,
             'description': 'SUV hạng B thiết kế cá tính, công nghệ hiện đại, giá cả cạnh tranh.',
             'features': ['Camera lùi', 'Cảnh báo điểm mù', 'Điều hòa tự động', 'Màn hình 10.25 inch', 'Sunroof'],
             'technical': {'power': '115 mã lực', 'torque': '144 Nm', 'consumption': '6.0L/100km', 'warranty': '3 năm'}},

            # KIA
            {'id': 10, 'brand': 'Kia', 'model': 'Seltos', 'year': 2023, 'price': 650000000, 'fuel_type': 'Xăng', 'engine_volume': '1.4L',
             'transmission': 'Số tự động', 'color': 'Cam', 'seats': 5,
             'description': 'SUV hạng B với thiết kế trẻ trung, động cơ tăng áp, tính năng an toàn đầy đủ.',
             'features': ['Camera lùi', 'Cảnh báo điểm mù', 'Điều hòa tự động', 'Màn hình 10.25 inch', 'Âm thanh Bose'],
             'technical': {'power': '140 mã lực', 'torque': '242 Nm', 'consumption': '6.2L/100km', 'warranty': '3 năm'}},

            {'id': 11, 'brand': 'Kia', 'model': 'K3', 'year': 2023, 'price': 590000000, 'fuel_type': 'Xăng', 'engine_volume': '1.6L',
             'transmission': 'CVT', 'color': 'Xám', 'seats': 5,
             'description': 'Sedan hạng C thiết kế thể thao, công nghệ hiện đại, vận hành êm ái.',
             'features': ['Camera lùi', 'Cảm biến lùi', 'Điều hòa tự động 2 vùng', 'Màn hình 10.25 inch', 'Ventilated seats'],
             'technical': {'power': '128 mã lực', 'torque': '157 Nm', 'consumption': '6.1L/100km', 'warranty': '3 năm'}},

            # MITSUBISHI
            {'id': 12, 'brand': 'Mitsubishi', 'model': 'Xpander', 'year': 2023, 'price': 560000000, 'fuel_type': 'Xăng', 'engine_volume': '1.5L',
             'transmission': 'CVT', 'color': 'Nâu', 'seats': 7,
             'description': 'MPV 7 chỗ bán chạy nhất phân khúc. Thiết kế Dynamic Shield, không gian linh hoạt.',
             'features': ['Camera lùi', 'Cảm biến lùi', 'Điều hòa tự động', 'Màn hình 9 inch', 'Cửa trượt điện'],
             'technical': {'power': '105 mã lực', 'torque': '141 Nm', 'consumption': '6.6L/100km', 'warranty': '3 năm'}},

            {'id': 13, 'brand': 'Mitsubishi', 'model': 'Triton', 'year': 2023, 'price': 680000000, 'fuel_type': 'Dầu', 'engine_volume': '2.4L',
             'transmission': 'Số tự động', 'color': 'Trắng', 'seats': 5,
             'description': 'Bán tải mạnh mẽ với hệ thống siêu chọn lọc 4WD, khả năng off-road vượt trội.',
             'features': ['Camera lùi', 'Cảm biến lùi', 'Điều hòa tự động', 'Màn hình 9 inch', 'Phanh điện tử'],
             'technical': {'power': '181 mã lực', 'torque': '430 Nm', 'consumption': '7.8L/100km', 'warranty': '3 năm'}},

            # MAZDA
            {'id': 14, 'brand': 'Mazda', 'model': 'CX-5', 'year': 2023, 'price': 890000000, 'fuel_type': 'Xăng', 'engine_volume': '2.0L',
             'transmission': 'Số tự động', 'color': 'Đỏ', 'seats': 5,
             'description': 'SUV hạng C với thiết kế KODO đẹp mắt, vận hành linh hoạt, nội thất sang trọng.',
             'features': ['Camera 360', 'Cảnh báo điểm mù', 'Điều hòa tự động 2 vùng', 'Màn hình 10.25 inch', 'Âm thanh Bose'],
             'technical': {'power': '154 mã lực', 'torque': '196 Nm', 'consumption': '6.7L/100km', 'warranty': '3 năm'}},

            {'id': 15, 'brand': 'Mazda', 'model': 'Mazda3', 'year': 2023, 'price': 720000000, 'fuel_type': 'Xăng', 'engine_volume': '1.5L',
             'transmission': 'Số tự động', 'color': 'Xám', 'seats': 5,
             'description': 'Sedan hạng C thiết kế thể thao, nội thất cao cấp, công nghệ an toàn i-ACTIVSENSE.',
             'features': ['Camera lùi', 'Cảnh báo điểm mù', 'Điều hòa tự động', 'Màn hình 8.8 inch', 'Heads-up display'],
             'technical': {'power': '118 mã lực', 'torque': '153 Nm', 'consumption': '5.9L/100km', 'warranty': '3 năm'}},

            # VINFAST
            {'id': 16, 'brand': 'VinFast', 'model': 'VF 5', 'year': 2023, 'price': 458000000, 'fuel_type': 'Điện', 'engine_volume': 'Điện',
             'transmission': 'Số tự động', 'color': 'Trắng', 'seats': 5,
             'description': 'XE điện cỡ A thông minh, thiết kế trẻ trung, phù hợp đô thị. Sạc nhanh 30 phút.',
             'features': ['Màn hình 10.1 inch', 'Kết nối 4G', 'Điều hòa tự động', 'Camera lùi', 'Hệ thống giải trí thông minh'],
             'technical': {'power': '118 mã lực', 'torque': '190 Nm', 'consumption': '11.5 kWh/100km', 'warranty': '7 năm'}},

            {'id': 17, 'brand': 'VinFast', 'model': 'VF e34', 'year': 2023, 'price': 690000000, 'fuel_type': 'Điện', 'engine_volume': 'Điện',
             'transmission': 'Số tự động', 'color': 'Xám', 'seats': 5,
             'description': 'XE điện cỡ C với trợ lý ảo thông minh, công nghệ Vingroup, bảo hành pin 10 năm.',
             'features': ['Trợ lý ảo', 'Màn hình 15.4 inch', 'Sạc nhanh DC', 'Cảnh báo điểm mù', 'Kết nối 5G'],
             'technical': {'power': '150 mã lực', 'torque': '242 Nm', 'consumption': '15.5 kWh/100km', 'warranty': '10 năm'}},

            # SUZUKI
            {'id': 18, 'brand': 'Suzuki', 'model': 'Ertiga', 'year': 2023, 'price': 520000000, 'fuel_type': 'Xăng', 'engine_volume': '1.5L',
             'transmission': 'CVT', 'color': 'Xanh', 'seats': 7,
             'description': 'MPV 7 chỗ giá rẻ, tiết kiệm nhiên liệu, phù hợp gia đình và kinh doanh vận tải.',
             'features': ['Camera lùi', 'Cảm biến lùi', 'Điều hòa tự động', 'Màn hình 8 inch', 'Túi khí đôi'],
             'technical': {'power': '105 mã lực', 'torque': '138 Nm', 'consumption': '6.2L/100km', 'warranty': '3 năm'}},

            # CHEVROLET
            {'id': 19, 'brand': 'Chevrolet', 'model': 'Colorado', 'year': 2023, 'price': 710000000, 'fuel_type': 'Dầu', 'engine_volume': '2.8L',
             'transmission': 'Số tự động', 'color': 'Đỏ', 'seats': 5,
             'description': 'Bán tải mạnh mẽ với động cơ Duramax, khả năng kéo tốt, thiết kế hiện đại.',
             'features': ['Camera lùi', 'Cảm biến lùi', 'Điều hòa tự động', 'Màn hình 8 inch', 'Apple CarPlay'],
             'technical': {'power': '200 mã lực', 'torque': '500 Nm', 'consumption': '8.5L/100km', 'warranty': '3 năm'}},
        ]

        # Chuyển đổi dữ liệu từ dictionary sang tuple
        car_data = []
        for car in cars:
            car_tuple = (
                car['brand'],
                car['model'],
                car['year'],
                car['engine_volume'],
                car['fuel_type'],
                car['transmission'],
                car['price'],
                car['color'],
                car['seats'],
                car['description'],
                ', '.join(car['features']),  # Chuyển list features thành string
                str(car['technical'])  # Chuyển dictionary technical thành string
            )
            car_data.append(car_tuple)

        insert_query = """INSERT INTO car (brand, model, year, engine_volume, fuel_type, transmission, 
                         price, color, seats, description, features, technical) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.executemany(insert_query, car_data)
        conn.commit()
        print(f"Đã thêm {cursor.rowcount} xe vào database")

    else:
        print("Dữ liệu đã tồn tại, không cần thêm mới")

    cursor.close()
    conn.close()

# Chạy chương trình
create_database()
create_table()
insert_sample_data()