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
            print("Ket noi thanh cong")
            return connection
    except Error as e:
        print("Loi ket noi {e}")
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
            engine_volume DECIMAL(3,1),
            fuel_type VARCHAR(20),
            transmission VARCHAR(20),
            km_driven INT,
            price BIGINT,
            color VARCHAR(30),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    print("Da tao bang thanh cong")

    cursor.close()
    conn.close()




def insert_sample_data():
    conn = create_connection()

    if conn is None:
        return
    
    cursor = conn.cursor()

    cursor.execute("select count(*) from car")
    count = cursor.fetchone()[0]

    if count == 0:

        car_database = [
            ('Toyota', 'Vios', 2020, 1.5, 'Xăng', 'Số sàn', 30000, 420000000, 'Trắng'),
            ('Toyota', 'Corolla Altis', 2021, 1.8, 'Xăng', 'CVT', 15000, 720000000, 'Đen'),
            ('Toyota', 'Camry', 2022, 2.5, 'Xăng', 'CVT', 10000, 1250000000, 'Bạc'),
            ('Toyota', 'Fortuner', 2021, 2.8, 'Dầu', 'Số tự động', 25000, 1350000000, 'Xám'),
            ('Toyota', 'Innova', 2020, 2.0, 'Xăng', 'Số tự động', 40000, 850000000, 'Trắng'),
            ('Toyota', 'Hiace', 2019, 2.8, 'Dầu', 'Số sàn', 80000, 750000000, 'Đen'),
            ('Toyota', 'Land Cruiser', 2023, 4.5, 'Xăng', 'Số tự động', 5000, 4500000000, 'Trắng'),
            ('Toyota', 'Raize', 2022, 1.0, 'Xăng', 'CVT', 12000, 420000000, 'Đỏ'),
            ('Honda', 'City', 2021, 1.5, 'Xăng', 'CVT', 20000, 580000000, 'Trắng'),
            ('Honda', 'Civic', 2022, 1.8, 'Xăng', 'CVT', 12000, 820000000, 'Đen'),
            ('Honda', 'CR-V', 2021, 1.5, 'Xăng', 'CVT', 18000, 980000000, 'Bạc'),
            ('Honda', 'Accord', 2020, 2.4, 'Xăng', 'CVT', 35000, 950000000, 'Xám'),
            ('Honda', 'HR-V', 2022, 1.5, 'Xăng', 'CVT', 10000, 720000000, 'Trắng'),
            ('Honda', 'BR-V', 2021, 1.5, 'Xăng', 'CVT', 22000, 620000000, 'Đen'),
            ('Honda', 'Brio', 2020, 1.2, 'Xăng', 'Số sàn', 45000, 380000000, 'Trắng'),
            ('Mercedes', 'C300', 2022, 2.0, 'Xăng', 'Số tự động', 8000, 2500000000, 'Đen'),
            ('Mercedes', 'E350', 2023, 3.0, 'Xăng', 'Số tự động', 5000, 3200000000, 'Trắng'),
            ('Mercedes', 'GLC300', 2022, 2.0, 'Xăng', 'Số tự động', 12000, 2800000000, 'Bạc'),
            ('Mercedes', 'S450', 2023, 3.0, 'Xăng', 'Số tự động', 3000, 4500000000, 'Đen'),
            ('Mercedes', 'G63', 2024, 4.0, 'Xăng', 'Số tự động', 1000, 8500000000, 'Đen'),
            ('Mercedes', 'C200', 2021, 1.5, 'Xăng', 'Số tự động', 18000, 2200000000, 'Trắng'),
            ('BMW', '320i', 2021, 2.0, 'Xăng', 'Số tự động', 15000, 1800000000, 'Trắng'),
            ('BMW', '520i', 2022, 2.0, 'Xăng', 'Số tự động', 9000, 2200000000, 'Đen'),
            ('BMW', 'X5', 2023, 3.0, 'Xăng', 'Số tự động', 7000, 3500000000, 'Xám'),
            ('BMW', 'X3', 2022, 2.0, 'Xăng', 'Số tự động', 11000, 2400000000, 'Bạc'),
            ('BMW', '730Li', 2023, 3.0, 'Xăng', 'Số tự động', 6000, 3800000000, 'Đen'),
            ('BMW', 'X1', 2021, 1.5, 'Xăng', 'Số tự động', 20000, 1600000000, 'Trắng'),
            ('Ford', 'Ranger', 2021, 2.0, 'Dầu', 'Số sàn', 45000, 680000000, 'Trắng'),
            ('Ford', 'Everest', 2022, 2.0, 'Dầu', 'Số tự động', 20000, 1100000000, 'Đen'),
            ('Ford', 'EcoSport', 2020, 1.5, 'Xăng', 'Số tự động', 55000, 520000000, 'Đỏ'),
            ('Ford', 'Explorer', 2023, 2.3, 'Xăng', 'Số tự động', 12000, 1300000000, 'Xám'),
            ('Ford', 'Focus', 2019, 1.5, 'Xăng', 'Số tự động', 65000, 550000000, 'Bạc'),
            ('Hyundai', 'Accent', 2020, 1.4, 'Xăng', 'Số sàn', 60000, 380000000, 'Trắng'),
            ('Hyundai', 'Elantra', 2021, 1.6, 'Xăng', 'CVT', 30000, 620000000, 'Đen'),
            ('Hyundai', 'Tucson', 2022, 1.6, 'Xăng', 'Số tự động', 15000, 850000000, 'Bạc'),
            ('Hyundai', 'Santa Fe', 2023, 2.5, 'Xăng', 'Số tự động', 8000, 1100000000, 'Xám'),
            ('Hyundai', 'Grand i10', 2020, 1.2, 'Xăng', 'Số sàn', 52000, 320000000, 'Trắng'),
            ('Kia', 'Cerato', 2021, 1.6, 'Xăng', 'Số sàn', 35000, 520000000, 'Trắng'),
            ('Kia', 'Seltos', 2022, 1.5, 'Xăng', 'CVT', 18000, 680000000, 'Đen'),
            ('Kia', 'Sportage', 2023, 1.6, 'Xăng', 'Số tự động', 12000, 920000000, 'Bạc'),
            ('Kia', 'Carnival', 2024, 2.2, 'Dầu', 'Số tự động', 5000, 1400000000, 'Xám'),
            ('Kia', 'K3', 2020, 1.5, 'Xăng', 'CVT', 42000, 480000000, 'Đỏ'),
            ('Mazda', 'CX-5', 2022, 2.0, 'Xăng', 'Số tự động', 22000, 920000000, 'Đỏ'),
            ('Mazda', 'CX-8', 2023, 2.5, 'Xăng', 'Số tự động', 13000, 1250000000, 'Trắng'),
            ('Mazda', 'Mazda3', 2021, 1.5, 'Xăng', 'CVT', 28000, 650000000, 'Đen'),
            ('Mazda', 'Mazda6', 2020, 2.0, 'Xăng', 'CVT', 35000, 720000000, 'Bạc'),
            ('VinFast', 'Lux A2.0', 2022, 2.0, 'Xăng', 'Số tự động', 18000, 1100000000, 'Trắng'),
            ('VinFast', 'Fadil', 2021, 1.4, 'Xăng', 'Số sàn', 42000, 380000000, 'Đen'),
            ('VinFast', 'VF e34', 2023, 1.5, 'Điện', 'Số tự động', 9000, 690000000, 'Xám'),
            ('VinFast', 'VF 8', 2023, 2.0, 'Điện', 'Số tự động', 5000, 1200000000, 'Đen'),
            ('Audi', 'A4', 2022, 2.0, 'Xăng', 'Số tự động', 12000, 2800000000, 'Đen'),
            ('Audi', 'Q5', 2023, 2.0, 'Xăng', 'Số tự động', 8000, 3200000000, 'Trắng'),
            ('Audi', 'Q7', 2021, 3.0, 'Xăng', 'Số tự động', 20000, 3500000000, 'Bạc'),
            ('Lexus', 'ES350', 2023, 3.5, 'Xăng', 'Số tự động', 7000, 3200000000, 'Trắng'),
            ('Lexus', 'RX350', 2022, 3.5, 'Xăng', 'Số tự động', 14000, 3500000000, 'Đen'),
            ('Lexus', 'NX350', 2023, 2.5, 'Xăng', 'Số tự động', 8000, 2800000000, 'Xám'),
            ('Porsche', 'Cayenne', 2023, 3.0, 'Xăng', 'Số tự động', 5000, 5500000000, 'Đen'),
            ('Porsche', 'Macan', 2022, 2.0, 'Xăng', 'Số tự động', 16000, 3200000000, 'Trắng'),
            ('Chevrolet', 'Spark', 2021, 1.2, 'Xăng', 'Số sàn', 65000, 320000000, 'Trắng'),
            ('Chevrolet', 'Trailblazer', 2023, 1.3, 'Xăng', 'CVT', 25000, 850000000, 'Đen'),
            ('Mitsubishi', 'Xpander', 2022, 1.5, 'Xăng', 'CVT', 32000, 620000000, 'Bạc'),
            ('Mitsubishi', 'Outlander', 2021, 2.4, 'Xăng', 'CVT', 38000, 780000000, 'Xám'),
            ('Suzuki', 'Ertiga', 2020, 1.5, 'Xăng', 'Số sàn', 48000, 420000000, 'Trắng'),
            ('Suzuki', 'Swift', 2022, 1.2, 'Xăng', 'CVT', 22000, 520000000, 'Đỏ'),
            ('Nissan', 'Sunny', 2019, 1.6, 'Xăng', 'CVT', 60000, 380000000, 'Bạc'),
            ('Nissan', 'X-Trail', 2021, 2.5, 'Xăng', 'CVT', 28000, 850000000, 'Đen')
        ]
    else:
        car_database = []

    insert_query = "insert into car (brand, model, year, engine_volume, fuel_type, transmission, km_driven, price, color) " \
    "values(%s, %s, %s, %s, %s, %s, %s, %s, %s)" 

    cursor.executemany(insert_query, car_database)

    conn.commit()

    print(cursor.rowcount)


create_database()
create_table()
insert_sample_data()
