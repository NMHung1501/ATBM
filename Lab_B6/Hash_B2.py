import hashlib
import os

def tinh_ma_bam_file(duong_dan_file: str):
    """Tính mã băm SHA-512 của một file bằng cách đọc từng khối dữ liệu."""
    if not os.path.exists(duong_dan_file):
        return "Lỗi: Không tìm thấy file!"

    doi_tuong_bam = hashlib.sha512()

    try:
        with open(duong_dan_file, 'rb') as f:
            for khoi_du_lieu in iter(lambda: f.read(4096), b""):
                doi_tuong_bam.update(khoi_du_lieu)
        return doi_tuong_bam.hexdigest()
    except Exception as e:
        return f"Lỗi khi đọc file: {e}"

def so_sanh_hai_file():
    """Nhập đường dẫn 2 file từ bàn phím và so sánh mã băm của chúng."""
    print("=== CHƯƠNG TRÌNH KIỂM TRA TÍNH TOÀN VẸN FILE ẢNH (SHA-512) ===")
    
    # 1. Yêu cầu nhập đường dẫn
    file_goc = input("Nhập đường dẫn file ảnh gốc (File 1): ").strip()
    file_kiem_tra = input("Nhập đường dẫn file ảnh cần kiểm tra (File 2): ").strip()

    print("\nĐang xử lý dữ liệu, vui lòng đợi...")

    # 2. Tính mã băm cho cả 2 file
    ma_bam_1 = tinh_ma_bam_file(file_goc)
    ma_bam_2 = tinh_ma_bam_file(file_kiem_tra)

    # Kiểm tra xem có lỗi khi đọc file không (VD: nhập sai tên file)
    if ma_bam_1.startswith("Lỗi"):
        print(f"[{file_goc}] -> {ma_bam_1}")
        return
    if ma_bam_2.startswith("Lỗi"):
        print(f"[{file_kiem_tra}] -> {ma_bam_2}")
        return

    # 3. In ra kết quả mã băm
    print(f"\n[+] Mã băm File 1: {ma_bam_1}")
    print(f"[+] Mã băm File 2: {ma_bam_2}\n")

    # 4. So sánh và kết luận
    if ma_bam_1 == ma_bam_2:
        print("=> KẾT QUẢ: Hai file HOÀN TOÀN GIỐNG NHAU (Giữ nguyên tính toàn vẹn).")
    else:
        print("=> KẾT QUẢ: Hai file KHÁC NHAU (File thứ hai đã bị chỉnh sửa hoặc hỏng).")

if __name__ == "__main__":
    so_sanh_hai_file()