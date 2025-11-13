import customtkinter as ctk
import requests
import json
from tkinter import messagebox
import threading

# Cấu hình giao diện
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class UngDungTraCuuXeHoi:
    def __init__(self):
        self.cua_so_chinh = ctk.CTk()
        self.cua_so_chinh.title("HỆ THỐNG TRA CỨU XE HƠI")
        self.cua_so_chinh.geometry("1400x800")

        # API endpoint
        self.url_goc = "http://localhost:5000"

        self.thiet_lap_giao_dien()
        self.tai_du_lieu_ban_dau()

    def thiet_lap_giao_dien(self):
        """Thiết lập giao diện người dùng"""
        # Header
        khung_tieu_de = ctk.CTkFrame(self.cua_so_chinh, fg_color="#ffffff", corner_radius=15)
        khung_tieu_de.pack(pady=20, padx=20, fill="x")

        # Tiêu đề
        nhan_tieu_de = ctk.CTkLabel(
            khung_tieu_de,
            text="🚗 HỆ THỐNG TRA CỨU XE HƠI",
            font=("Arial", 24, "bold"),
            text_color="#333333"
        )
        nhan_tieu_de.pack(pady=15)

        nhan_phu_de = ctk.CTkLabel(
            khung_tieu_de,
            text="Database 70+ mẫu xe - Tìm kiếm thông tin chi tiết",
            font=("Arial", 14),
            text_color="#666666"
        )
        nhan_phu_de.pack(pady=5)

        # Main content
        khung_chinh = ctk.CTkFrame(self.cua_so_chinh, fg_color="transparent")
        khung_chinh.pack(fill="both", expand=True, padx=20, pady=10)

        # Tạo layout 2 cột
        khung_chinh.grid_columnconfigure(1, weight=1)
        khung_chinh.grid_rowconfigure(0, weight=1)

        # Cột trái - Bộ lọc
        self.thiet_lap_cot_loc(khung_chinh)

        # Cột phải - Kết quả
        self.thiet_lap_cot_ket_qua(khung_chinh)

    def thiet_lap_cot_loc(self, cha):
        """Thiết lập cột bộ lọc"""
        khung_loc = ctk.CTkFrame(cha, fg_color="#ffffff", corner_radius=15)
        khung_loc.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Tiêu đề bộ lọc
        tieu_de_loc = ctk.CTkLabel(
            khung_loc,
            text="🔍 TÌM KIẾM",
            font=("Arial", 18, "bold"),
            text_color="#333333"
        )
        tieu_de_loc.pack(pady=15)

        # Hãng xe
        nhan_hang_xe = ctk.CTkLabel(khung_loc, text="Hãng xe:", text_color="#333333")
        nhan_hang_xe.pack(anchor="w", padx=20, pady=(10, 5))

        self.combo_hang_xe = ctk.CTkComboBox(
            khung_loc,
            values=["Đang tải..."],
            state="readonly",
            width=250
        )
        self.combo_hang_xe.pack(padx=20, pady=(0, 15))

        # Dòng xe
        nhan_dong_xe = ctk.CTkLabel(khung_loc, text="Dòng xe:", text_color="#333333")
        nhan_dong_xe.pack(anchor="w", padx=20, pady=(10, 5))

        self.entry_dong_xe = ctk.CTkEntry(
            khung_loc,
            placeholder_text="Nhập tên dòng xe...",
            width=250
        )
        self.entry_dong_xe.pack(padx=20, pady=(0, 15))

        # Năm sản xuất
        khung_nam = ctk.CTkFrame(khung_loc, fg_color="transparent")
        khung_nam.pack(fill="x", padx=20, pady=(10, 5))

        nhan_nam = ctk.CTkLabel(khung_nam, text="Năm sản xuất:", text_color="#333333")
        nhan_nam.pack(anchor="w")

        khung_nhap_nam = ctk.CTkFrame(khung_loc, fg_color="transparent")
        khung_nhap_nam.pack(fill="x", padx=20, pady=(0, 15))

        self.entry_nam_toi_thieu = ctk.CTkEntry(khung_nhap_nam, placeholder_text="Từ năm", width=120)
        self.entry_nam_toi_thieu.pack(side="left", padx=(0, 10))
        self.entry_nam_toi_thieu.insert(0, "2018")

        self.entry_nam_toi_da = ctk.CTkEntry(khung_nhap_nam, placeholder_text="Đến năm", width=120)
        self.entry_nam_toi_da.pack(side="left")
        self.entry_nam_toi_da.insert(0, "2024")

        # Loại nhiên liệu
        nhan_nhien_lieu = ctk.CTkLabel(khung_loc, text="Loại nhiên liệu:", text_color="#333333")
        nhan_nhien_lieu.pack(anchor="w", padx=20, pady=(10, 5))

        self.combo_nhien_lieu = ctk.CTkComboBox(
            khung_loc,
            values=["Tất cả", "Xăng", "Dầu", "Điện"],
            state="readonly",
            width=250
        )
        self.combo_nhien_lieu.set("Tất cả")
        self.combo_nhien_lieu.pack(padx=20, pady=(0, 25))

        # Nút tìm kiếm
        self.nut_tim_kiem = ctk.CTkButton(
            khung_loc,
            text="🔍 TÌM KIẾM",
            command=self.tim_kiem_xe,
            height=45,
            font=("Arial", 14, "bold")
        )
        self.nut_tim_kiem.pack(padx=20, pady=10)

    def thiet_lap_cot_ket_qua(self, cha):
        """Thiết lập cột kết quả"""
        khung_ket_qua = ctk.CTkFrame(cha, fg_color="#ffffff", corner_radius=15)
        khung_ket_qua.grid(row=0, column=1, sticky="nsew")

        # Tiêu đề kết quả
        tieu_de_ket_qua = ctk.CTkLabel(
            khung_ket_qua,
            text="📊 KẾT QUẢ TRA CỨU",
            font=("Arial", 18, "bold"),
            text_color="#333333"
        )
        tieu_de_ket_qua.pack(pady=15)

        # Thống kê
        self.thiet_lap_phan_thong_ke(khung_ket_qua)

        # Kết quả tìm kiếm
        self.thiet_lap_phan_ket_qua(khung_ket_qua)

    def thiet_lap_phan_thong_ke(self, cha):
        """Thiết lập phần thống kê"""
        khung_thong_ke = ctk.CTkFrame(cha, fg_color="#f8f9fa", corner_radius=10)
        khung_thong_ke.pack(fill="x", padx=20, pady=(0, 20))

        # Grid cho thống kê
        khung_thong_ke.grid_columnconfigure(0, weight=1)
        khung_thong_ke.grid_columnconfigure(1, weight=1)
        khung_thong_ke.grid_columnconfigure(2, weight=1)
        khung_thong_ke.grid_columnconfigure(3, weight=1)

        # Tổng số xe
        self.nhan_tong_xe = ctk.CTkLabel(
            khung_thong_ke,
            text="-",
            font=("Arial", 20, "bold"),
            text_color="#007bff"
        )
        self.nhan_tong_xe.grid(row=0, column=0, pady=15)

        nhan_chu_tong_xe = ctk.CTkLabel(
            khung_thong_ke,
            text="TỔNG SỐ XE",
            font=("Arial", 12),
            text_color="#666666"
        )
        nhan_chu_tong_xe.grid(row=1, column=0, pady=(0, 15))

        # Hãng xe
        self.nhan_tong_hang_xe = ctk.CTkLabel(
            khung_thong_ke,
            text="-",
            font=("Arial", 20, "bold"),
            text_color="#007bff"
        )
        self.nhan_tong_hang_xe.grid(row=0, column=1, pady=15)

        nhan_chu_tong_hang_xe = ctk.CTkLabel(
            khung_thong_ke,
            text="HÃNG XE",
            font=("Arial", 12),
            text_color="#666666"
        )
        nhan_chu_tong_hang_xe.grid(row=1, column=1, pady=(0, 15))

        # Mẫu xe
        self.nhan_tong_mau_xe = ctk.CTkLabel(
            khung_thong_ke,
            text="-",
            font=("Arial", 20, "bold"),
            text_color="#007bff"
        )
        self.nhan_tong_mau_xe.grid(row=0, column=2, pady=15)

        nhan_chu_tong_mau_xe = ctk.CTkLabel(
            khung_thong_ke,
            text="MẪU XE",
            font=("Arial", 12),
            text_color="#666666"
        )
        nhan_chu_tong_mau_xe.grid(row=1, column=2, pady=(0, 15))

        # Giá trung bình
        self.nhan_gia_trung_binh = ctk.CTkLabel(
            khung_thong_ke,
            text="-",
            font=("Arial", 16, "bold"),
            text_color="#007bff"
        )
        self.nhan_gia_trung_binh.grid(row=0, column=3, pady=15)

        nhan_chu_gia_trung_binh = ctk.CTkLabel(
            khung_thong_ke,
            text="GIÁ TRUNG BÌNH",
            font=("Arial", 12),
            text_color="#666666"
        )
        nhan_chu_gia_trung_binh.grid(row=1, column=3, pady=(0, 15))

    def thiet_lap_phan_ket_qua(self, cha):
        """Thiết lập phần kết quả"""
        # Frame cho kết quả
        khung_noi_dung_ket_qua = ctk.CTkFrame(cha, fg_color="transparent")
        khung_noi_dung_ket_qua.pack(fill="both", expand=True, padx=20, pady=10)

        # Label số lượng kết quả
        self.nhan_so_luong_ket_qua = ctk.CTkLabel(
            khung_noi_dung_ket_qua,
            text="Nhập tiêu chí và nhấn TÌM KIẾM để xem kết quả",
            font=("Arial", 14),
            text_color="#333333"
        )
        self.nhan_so_luong_ket_qua.pack(anchor="w", pady=(0, 15))

        # Scrollable frame cho kết quả
        self.khung_cuon_ket_qua = ctk.CTkScrollableFrame(
            khung_noi_dung_ket_qua,
            fg_color="transparent"
        )
        self.khung_cuon_ket_qua.pack(fill="both", expand=True)

    def tai_du_lieu_ban_dau(self):
        """Load dữ liệu ban đầu"""
        threading.Thread(target=self.tai_danh_sach_hang_xe, daemon=True).start()
        threading.Thread(target=self.tai_thong_ke, daemon=True).start()

    def tai_danh_sach_hang_xe(self):
        """Load danh sách hãng xe từ API"""
        try:
            phan_hoi = requests.get(f"{self.url_goc}/api/brands")
            if phan_hoi.status_code == 200:
                du_lieu = phan_hoi.json()
                danh_sach_hang_xe = ["Tất cả hãng xe"] + du_lieu['brands']
                self.combo_hang_xe.configure(values=danh_sach_hang_xe)
                self.combo_hang_xe.set("Tất cả hãng xe")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể load danh sách hãng xe: {e}")

    def tai_thong_ke(self):
        """Load thống kê từ API"""
        try:
            phan_hoi = requests.get(f"{self.url_goc}/api/stats")
            if phan_hoi.status_code == 200:
                du_lieu = phan_hoi.json()
                self.nhan_tong_xe.configure(text=du_lieu['total_cars'])
                self.nhan_tong_hang_xe.configure(text=du_lieu['total_brands'])
                self.nhan_tong_mau_xe.configure(text=du_lieu['total_models'])
                self.nhan_gia_trung_binh.configure(text=du_lieu['avg_price'])
        except Exception as e:
            print(f"Lỗi load stats: {e}")

    def tim_kiem_xe(self):
        """Tìm kiếm xe"""
        threading.Thread(target=self._luong_tim_kiem_xe, daemon=True).start()

    def _luong_tim_kiem_xe(self):
        """Thread tìm kiếm xe"""
        try:
            # Cập nhật UI
            self.nut_tim_kiem.configure(state="disabled", text="🔄 ĐANG TÌM KIẾM...")

            # Lấy giá trị từ form
            bo_loc = {
                'brand': self.combo_hang_xe.get() if self.combo_hang_xe.get() != "Tất cả hãng xe" else '',
                'model': self.entry_dong_xe.get(),
                'min_year': int(self.entry_nam_toi_thieu.get()),
                'max_year': int(self.entry_nam_toi_da.get()),
                'fuel_type': self.combo_nhien_lieu.get() if self.combo_nhien_lieu.get() != "Tất cả" else ''
            }

            # Gọi API
            phan_hoi = requests.post(f"{self.url_goc}/api/search", json=bo_loc)

            if phan_hoi.status_code == 200:
                du_lieu = phan_hoi.json()
                self.hien_thi_ket_qua(du_lieu)
            else:
                messagebox.showerror("Lỗi", "Không thể kết nối đến server")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tìm kiếm: {e}")
        finally:
            # Khôi phục button
            self.nut_tim_kiem.configure(state="normal", text="🔍 TÌM KIẾM")

    def hien_thi_ket_qua(self, du_lieu):
        """Hiển thị kết quả tìm kiếm"""
        # Xóa kết quả cũ
        for widget in self.khung_cuon_ket_qua.winfo_children():
            widget.destroy()

        if du_lieu['success']:
            ket_qua = du_lieu['results']
            so_luong = du_lieu['count']

            # Cập nhật số lượng kết quả
            if so_luong > 0:
                self.nhan_so_luong_ket_qua.configure(
                    text=f"📊 Tìm thấy {so_luong} xe phù hợp",
                    text_color="#333333"
                )
            else:
                self.nhan_so_luong_ket_qua.configure(
                    text="❌ Không tìm thấy xe phù hợp",
                    text_color="#dc3545"
                )

            # Hiển thị kết quả
            for xe in ket_qua:
                self.tao_the_xe(xe)
        else:
            self.nhan_so_luong_ket_qua.configure(
                text=f"❌ Lỗi: {du_lieu['error']}",
                text_color="#dc3545"
            )

    def tao_the_xe(self, xe):
        """Tạo card hiển thị thông tin xe"""
        khung_the = ctk.CTkFrame(
            self.khung_cuon_ket_qua,
            fg_color="#f8f9fa",
            corner_radius=10,
            border_width=1,
            border_color="#e1e5e9"
        )
        khung_the.pack(fill="x", pady=5)

        # Header card
        khung_tieu_de_the = ctk.CTkFrame(khung_the, fg_color="transparent")
        khung_tieu_de_the.pack(fill="x", padx=15, pady=10)

        # Hãng xe và năm
        nhan_hang_xe = ctk.CTkLabel(
            khung_tieu_de_the,
            text=xe['brand'],
            font=("Arial", 16, "bold"),
            text_color="#333333"
        )
        nhan_hang_xe.pack(side="left")

        nhan_nam = ctk.CTkLabel(
            khung_tieu_de_the,
            text=str(xe['year']),
            font=("Arial", 12, "bold"),
            text_color="#ffffff",
            fg_color="#007bff",
            corner_radius=8
        )
        nhan_nam.pack(side="right", padx=(10, 0))

        # Dòng xe
        nhan_dong_xe = ctk.CTkLabel(
            khung_the,
            text=xe['model'],
            font=("Arial", 14),
            text_color="#666666"
        )
        nhan_dong_xe.pack(anchor="w", padx=15, pady=(0, 10))

        # Giá
        nhan_gia = ctk.CTkLabel(
            khung_the,
            text=xe['price'],
            font=("Arial", 18, "bold"),
            text_color="#28a745"
        )
        nhan_gia.pack(anchor="w", padx=15, pady=(0, 15))

        # Thông tin chi tiết
        khung_chi_tiet = ctk.CTkFrame(khung_the, fg_color="transparent")
        khung_chi_tiet.pack(fill="x", padx=15, pady=(0, 10))

        # Grid cho chi tiết
        khung_chi_tiet.grid_columnconfigure(0, weight=1)
        khung_chi_tiet.grid_columnconfigure(1, weight=1)
        khung_chi_tiet.grid_columnconfigure(2, weight=1)
        khung_chi_tiet.grid_columnconfigure(3, weight=1)

        # Động cơ
        nhan_dong_co = ctk.CTkLabel(
            khung_chi_tiet,
            text=f"⚙️ {xe['engine_volume']}",
            font=("Arial", 12),
            text_color="#333333"
        )
        nhan_dong_co.grid(row=0, column=0, sticky="w")

        # Nhiên liệu
        nhan_nhien_lieu = ctk.CTkLabel(
            khung_chi_tiet,
            text=f"⛽ {xe['fuel_type']}",
            font=("Arial", 12),
            text_color="#333333"
        )
        nhan_nhien_lieu.grid(row=0, column=1, sticky="w")

        # Hộp số
        nhan_hop_so = ctk.CTkLabel(
            khung_chi_tiet,
            text=f"🔧 {xe['transmission']}",
            font=("Arial", 12),
            text_color="#333333"
        )
        nhan_hop_so.grid(row=0, column=2, sticky="w")

        # Số km
        nhan_so_km = ctk.CTkLabel(
            khung_chi_tiet,
            text=f"🛣️ {xe['km_driven']}",
            font=("Arial", 12),
            text_color="#333333"
        )
        nhan_so_km.grid(row=0, column=3, sticky="w")

        # Màu xe
        nhan_mau_xe = ctk.CTkLabel(
            khung_the,
            text=f"🎨 Màu: {xe['color']}",
            font=("Arial", 11),
            text_color="#666666"
        )
        nhan_mau_xe.pack(anchor="w", padx=15, pady=(0, 10))

    def chay_ung_dung(self):
        """Chạy ứng dụng"""
        self.cua_so_chinh.mainloop()


if __name__ == "__main__":
    print("🚗 KHỞI ĐỘNG ỨNG DỤNG TRA CỨU XE HƠI")
    print("📡 Đang kết nối đến: http://localhost:5000")

    ung_dung = UngDungTraCuuXeHoi()
    ung_dung.chay_ung_dung()