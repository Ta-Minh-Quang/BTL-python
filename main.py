from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from flask_cors import CORS
from mysql.connector import Error
from connectdb import create_connection
import customtkinter as ctk
import threading

app = Flask(__name__)
CORS(app)


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


df = get_cars_dataframe()
if df is not None:
    print(f"📊 Loaded {len(df)} cars from MySQL")
    print(df.head())

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


# ================== THÊM GUI ==================
def start_gui():
    """Khởi động GUI ứng dụng"""
    app_gui = ctk.CTk()
    app_gui.title("HỆ THỐNG TRA CỨU XE HƠI - GUI")
    app_gui.geometry("800x600")

    title_label = ctk.CTkLabel(
        app_gui,
        text="🚗 HỆ THỐNG TRA CỨU XE HƠI",
        font=("Arial", 20, "bold")
    )
    title_label.pack(pady=20)

    info_label = ctk.CTkLabel(
        app_gui,
        text="✅ Flask API đang chạy tại: http://localhost:5000\n✅ GUI ứng dụng đã sẵn sàng",
        font=("Arial", 14)
    )
    info_label.pack(pady=10)

    stats_label = ctk.CTkLabel(
        app_gui,
        text=f"📊 Đã tải {len(df)} xe từ database",
        font=("Arial", 12)
    )
    stats_label.pack(pady=5)

    app_gui.mainloop()


if __name__ == '__main__':
    print("🚗 KHỞI ĐỘNG HỆ THỐNG TRA CỨU XE HƠI")
    print(f"📊 Tổng số xe trong database: {len(df)}")
    print(f"🏷️ Số hãng xe: {len(df['brand'].unique())}")
    print(f"🚀 Số mẫu xe: {len(df['model'].unique())}")
    print(f"💰 Giá trung bình: {df['price'].mean():,.0f} VND")

    # Chạy GUI trong thread riêng
    gui_thread = threading.Thread(target=start_gui, daemon=True)
    gui_thread.start()

    # Chạy Flask server
    app.run(debug=True, port=5000, host='0.0.0.0')