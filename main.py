from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from mysql.connector import Error

from connectdb import create_connection




app = Flask(__name__)



def get_cars_dataframe():
    conn = create_connection()
    if conn is None:
        return None
    try:
        query = "select * from car"
        df = pd.read_sql(query, conn)
        return df
    except Error as e:
        print(f"Lỗi đọc dữ liệu; {e}")
        return None
    finally:
        conn.close()



# DATABASE XE HƠI ĐẦY ĐỦ
# car_database = {
#     'brand': [
#         'Toyota', 'Toyota', 'Toyota', 'Toyota', 'Toyota', 'Toyota', 'Toyota', 'Toyota',
#         'Honda', 'Honda', 'Honda', 'Honda', 'Honda', 'Honda', 'Honda',
#         'Mercedes', 'Mercedes', 'Mercedes', 'Mercedes', 'Mercedes', 'Mercedes',
#         'BMW', 'BMW', 'BMW', 'BMW', 'BMW', 'BMW',
#         'Ford', 'Ford', 'Ford', 'Ford', 'Ford',
#         'Hyundai', 'Hyundai', 'Hyundai', 'Hyundai', 'Hyundai',
#         'Kia', 'Kia', 'Kia', 'Kia', 'Kia',
#         'Mazda', 'Mazda', 'Mazda', 'Mazda',
#         'VinFast', 'VinFast', 'VinFast', 'VinFast',
#         'Audi', 'Audi', 'Audi',
#         'Lexus', 'Lexus', 'Lexus',
#         'Porsche', 'Porsche',
#         'Chevrolet', 'Chevrolet',
#         'Mitsubishi', 'Mitsubishi',
#         'Suzuki', 'Suzuki',
#         'Nissan', 'Nissan'
#     ],
#     'model': [
#         'Vios', 'Corolla Altis', 'Camry', 'Fortuner', 'Innova', 'Hiace', 'Land Cruiser', 'Raize',
#         'City', 'Civic', 'CR-V', 'Accord', 'HR-V', 'BR-V', 'Brio',
#         'C300', 'E350', 'GLC300', 'S450', 'G63', 'C200',
#         '320i', '520i', 'X5', 'X3', '730Li', 'X1',
#         'Ranger', 'Everest', 'EcoSport', 'Explorer', 'Focus',
#         'Accent', 'Elantra', 'Tucson', 'Santa Fe', 'Grand i10',
#         'Cerato', 'Seltos', 'Sportage', 'Carnival', 'K3',
#         'CX-5', 'CX-8', 'Mazda3', 'Mazda6',
#         'Lux A2.0', 'Fadil', 'VF e34', 'VF 8',
#         'A4', 'Q5', 'Q7',
#         'ES350', 'RX350', 'NX350',
#         'Cayenne', 'Macan',
#         'Spark', 'Trailblazer',
#         'Xpander', 'Outlander',
#         'Ertiga', 'Swift',
#         'Sunny', 'X-Trail'
#     ],
#     'year': [
#         2020, 2021, 2022, 2021, 2020, 2019, 2023, 2022,
#         2021, 2022, 2021, 2020, 2022, 2021, 2020,
#         2022, 2023, 2022, 2023, 2024, 2021,
#         2021, 2022, 2023, 2022, 2023, 2021,
#         2021, 2022, 2020, 2023, 2019,
#         2020, 2021, 2022, 2023, 2020,
#         2021, 2022, 2023, 2024, 2020,
#         2022, 2023, 2021, 2020,
#         2022, 2021, 2023, 2023,
#         2022, 2023, 2021,
#         2023, 2022, 2023,
#         2023, 2022,
#         2021, 2023,
#         2022, 2021,
#         2020, 2022,
#         2019, 2021
#     ],
#     'engine_volume': [
#         1.5, 1.8, 2.5, 2.8, 2.0, 2.8, 4.5, 1.0,
#         1.5, 1.8, 1.5, 2.4, 1.5, 1.5, 1.2,
#         2.0, 3.0, 2.0, 3.0, 4.0, 1.5,
#         2.0, 2.0, 3.0, 2.0, 3.0, 1.5,
#         2.0, 2.0, 1.5, 2.3, 1.5,
#         1.4, 1.6, 1.6, 2.5, 1.2,
#         1.6, 1.5, 1.6, 2.2, 1.5,
#         2.0, 2.5, 1.5, 2.0,
#         2.0, 1.4, 1.5, 2.0,
#         2.0, 2.0, 3.0,
#         3.5, 3.5, 2.5,
#         3.0, 2.0,
#         1.2, 1.3,
#         1.5, 2.4,
#         1.5, 1.2,
#         1.6, 2.5
#     ],
#     'fuel_type': [
#         'Xăng', 'Xăng', 'Xăng', 'Dầu', 'Xăng', 'Dầu', 'Xăng', 'Xăng',
#         'Xăng', 'Xăng', 'Xăng', 'Xăng', 'Xăng', 'Xăng', 'Xăng',
#         'Xăng', 'Xăng', 'Xăng', 'Xăng', 'Xăng', 'Xăng',
#         'Xăng', 'Xăng', 'Xăng', 'Xăng', 'Xăng', 'Xăng',
#         'Dầu', 'Dầu', 'Xăng', 'Xăng', 'Xăng',
#         'Xăng', 'Xăng', 'Xăng', 'Xăng', 'Xăng',
#         'Xăng', 'Xăng', 'Xăng', 'Dầu', 'Xăng',
#         'Xăng', 'Xăng', 'Xăng', 'Xăng',
#         'Xăng', 'Xăng', 'Điện', 'Điện',
#         'Xăng', 'Xăng', 'Xăng',
#         'Xăng', 'Xăng', 'Xăng',
#         'Xăng', 'Xăng',
#         'Xăng', 'Xăng',
#         'Xăng', 'Xăng',
#         'Xăng', 'Xăng',
#         'Xăng', 'Xăng'
#     ],
#     'transmission': [
#         'Số sàn', 'CVT', 'CVT', 'Số tự động', 'Số tự động', 'Số sàn', 'Số tự động', 'CVT',
#         'CVT', 'CVT', 'CVT', 'CVT', 'CVT', 'CVT', 'Số sàn',
#         'Số tự động', 'Số tự động', 'Số tự động', 'Số tự động', 'Số tự động', 'Số tự động',
#         'Số tự động', 'Số tự động', 'Số tự động', 'Số tự động', 'Số tự động', 'Số tự động',
#         'Số sàn', 'Số tự động', 'Số tự động', 'Số tự động', 'Số tự động',
#         'Số sàn', 'CVT', 'Số tự động', 'Số tự động', 'Số sàn',
#         'Số sàn', 'CVT', 'Số tự động', 'Số tự động', 'CVT',
#         'Số tự động', 'Số tự động', 'CVT', 'CVT',
#         'Số tự động', 'Số sàn', 'Số tự động', 'Số tự động',
#         'Số tự động', 'Số tự động', 'Số tự động',
#         'Số tự động', 'Số tự động', 'Số tự động',
#         'Số tự động', 'Số tự động',
#         'Số sàn', 'CVT',
#         'CVT', 'CVT',
#         'Số sàn', 'CVT',
#         'CVT', 'CVT'
#     ],
#     'km_driven': [
#         30000, 15000, 10000, 25000, 40000, 80000, 5000, 12000,
#         20000, 12000, 18000, 35000, 10000, 22000, 45000,
#         8000, 5000, 12000, 3000, 1000, 18000,
#         15000, 9000, 7000, 11000, 6000, 20000,
#         45000, 20000, 55000, 12000, 65000,
#         60000, 30000, 15000, 8000, 52000,
#         35000, 18000, 12000, 5000, 42000,
#         22000, 13000, 28000, 35000,
#         18000, 42000, 9000, 5000,
#         12000, 8000, 20000,
#         7000, 14000, 8000,
#         5000, 16000,
#         65000, 25000,
#         32000, 38000,
#         48000, 22000,
#         60000, 28000
#     ],
#     'price': [
#         420000000, 720000000, 1250000000, 1350000000, 850000000, 750000000, 4500000000, 420000000,
#         580000000, 820000000, 980000000, 950000000, 720000000, 620000000, 380000000,
#         2500000000, 3200000000, 2800000000, 4500000000, 8500000000, 2200000000,
#         1800000000, 2200000000, 3500000000, 2400000000, 3800000000, 1600000000,
#         680000000, 1100000000, 520000000, 1300000000, 550000000,
#         380000000, 620000000, 850000000, 1100000000, 320000000,
#         520000000, 680000000, 920000000, 1400000000, 480000000,
#         920000000, 1250000000, 650000000, 720000000,
#         1100000000, 380000000, 690000000, 1200000000,
#         2800000000, 3200000000, 3500000000,
#         3200000000, 3500000000, 2800000000,
#         5500000000, 3200000000,
#         320000000, 850000000,
#         620000000, 780000000,
#         420000000, 520000000,
#         380000000, 850000000
#     ],
#     'color': [
#         'Trắng', 'Đen', 'Bạc', 'Xám', 'Trắng', 'Đen', 'Trắng', 'Đỏ',
#         'Trắng', 'Đen', 'Bạc', 'Xám', 'Trắng', 'Đen', 'Trắng',
#         'Đen', 'Trắng', 'Bạc', 'Đen', 'Đen', 'Trắng',
#         'Trắng', 'Đen', 'Xám', 'Bạc', 'Đen', 'Trắng',
#         'Trắng', 'Đen', 'Đỏ', 'Xám', 'Bạc',
#         'Trắng', 'Đen', 'Bạc', 'Xám', 'Trắng',
#         'Trắng', 'Đen', 'Bạc', 'Xám', 'Đỏ',
#         'Đỏ', 'Trắng', 'Đen', 'Bạc',
#         'Trắng', 'Đen', 'Xám', 'Đen',
#         'Đen', 'Trắng', 'Bạc',
#         'Trắng', 'Đen', 'Xám',
#         'Đen', 'Trắng',
#         'Trắng', 'Đen',
#         'Bạc', 'Xám',
#         'Trắng', 'Đỏ',
#         'Bạc', 'Đen'
#     ]
# }

# Tạo DataFrame
# df = pd.DataFrame(car_database)

df = get_cars_dataframe()
if df is not None:
    print(f"📊 Loaded {len(df)} cars from MySQL")
    print(df.head())
    



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/stats')
def get_stats():
    """API trả về thống kê hệ thống"""
    stats = {
        'total_cars': len(df),
        'total_brands': len(df['brand'].unique()),
        'total_models': len(df['model'].unique()),
        'avg_price': f"{df['price'].mean():,.0f} VND",
        'min_year': int(df['year'].min()),
        'max_year': int(df['year'].max())
    }
    return jsonify(stats)


@app.route('/api/brands')
def get_brands():
    """API trả về danh sách hãng xe"""
    brands = sorted(df['brand'].unique().tolist())
    return jsonify({'brands': brands})


@app.route('/api/models/<brand>')
def get_models(brand):
    """API trả về danh sách mẫu xe theo hãng"""
    models = df[df['brand'] == brand]['model'].unique().tolist()
    return jsonify({'models': sorted(models)})


@app.route('/api/search', methods=['POST'])
def search_cars():
    """API tìm kiếm xe với bộ lọc"""
    try:
        data = request.json
        brand = data.get('brand', '')
        model = data.get('model', '')
        min_year = data.get('min_year', 2000)
        max_year = data.get('max_year', 2024)
        fuel_type = data.get('fuel_type', '')

        # Lọc xe
        filtered_cars = df.copy()

        if brand:
            filtered_cars = filtered_cars[filtered_cars['brand'].str.contains(brand, case=False)]

        if model:
            filtered_cars = filtered_cars[filtered_cars['model'].str.contains(model, case=False)]

        if fuel_type:
            filtered_cars = filtered_cars[filtered_cars['fuel_type'] == fuel_type]

        filtered_cars = filtered_cars[
            (filtered_cars['year'] >= min_year) &
            (filtered_cars['year'] <= max_year)
            ]
        
        filtered_cars = filtered_cars.drop_duplicates(
            subset=['brand', 'model', 'year', 'color', 'price']
        )


        # Sắp xếp theo giá
        filtered_cars = filtered_cars.sort_values('price')

        results = []
        for _, car in filtered_cars.iterrows():
            results.append({
                'brand': car['brand'],
                'model': car['model'],
                'year': int(car['year']),
                'price': f"{car['price']:,.0f} VND",
                'engine_volume': f"{car['engine_volume']}L",
                'fuel_type': car['fuel_type'],
                'transmission': car['transmission'],
                'km_driven': f"{car['km_driven']:,.0f} km",
                'color': car['color']
            })

        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    print("🚗 KHỞI ĐỘNG HỆ THỐNG TRA CỨU XE HƠI")
    print(f"📊 Tổng số xe trong database: {len(df)}")
    print(f"🏷️ Số hãng xe: {len(df['brand'].unique())}")
    print(f"🚀 Số mẫu xe: {len(df['model'].unique())}")
    print(f"💰 Giá trung bình: {df['price'].mean():,.0f} VND")
    app.run(debug=True, port=5000)