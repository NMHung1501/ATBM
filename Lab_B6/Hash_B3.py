import hashlib
import shutil
import os

def tinh_ma_bam(duong_dan_file):
    if not os.path.exists(duong_dan_file):
        return None
        
    doi_tuong_bam = hashlib.sha256()
    with open(duong_dan_file, 'rb') as f:
        for khoi_du_lieu in iter(lambda: f.read(4096), b""):
            doi_tuong_bam.update(khoi_du_lieu)
    return doi_tuong_bam.hexdigest()

def mo_phong_truyen_file(file_goc, file_nhan, bi_tan_cong=False):

    print(f"\n{'='*40}")
    print(" [1] BÊN GỬI (SENDER) ĐANG XỬ LÝ")
    print(f"{'='*40}")
    
    ma_bam_goc = tinh_ma_bam(file_goc)
    if not ma_bam_goc:
        print(f"Lỗi: Không tìm thấy file gốc '{file_goc}' để gửi!")
        return
        
    print(f"File cần gửi: {file_goc}")
    print(f"Mã băm gốc (SHA-256): {ma_bam_goc}")
    print("Đang truyền dữ liệu qua mạng (Copying file)...")

    try:
        shutil.copyfile(file_goc, file_nhan)
    except Exception as e:
        print(f"Lỗi trong quá trình truyền file: {e}")
        return

    if bi_tan_cong:
        print(">>> CẢNH BÁO: Hacker đang chèn mã độc vào file trên đường truyền! <<<")
        with open(file_nhan, 'ab') as f:
            f.write(b"Malicious Code Inserted Here!")

    print(f"\n{'='*40}")
    print(" [2] BÊN NHẬN (RECEIVER) ĐANG XỬ LÝ")
    print(f"{'='*40}")
    
    print(f"Đã nhận file tại: {file_nhan}")
    ma_bam_nhan_duoc = tinh_ma_bam(file_nhan)
    print(f"Mã băm tự tính (SHA-256): {ma_bam_nhan_duoc}")

    print(f"\n{'='*40}")
    print(" [3] XÁC THỰC TÍNH TOÀN VẸN (INTEGRITY CHECK)")
    print(f"{'='*40}")
    
    if ma_bam_goc == ma_bam_nhan_duoc:
        print("=> SUCCESS: Trùng khớp! File được truyền tải an toàn 100%.")
    else:
        print("=> FAILED: Phát hiện sai lệch! File đã bị hỏng hoặc bị hacker can thiệp.")


if __name__ == "__main__":
    file_mau = "data_goc.txt"
    with open(file_mau, "w") as f:
        f.write("Day la du lieu mat cua cong ty.")

    file_dich = "data_da_nhan.txt"

    print("\n--- KỊCH BẢN 1: ĐƯỜNG TRUYỀN AN TOÀN ---")
    mo_phong_truyen_file(file_mau, file_dich, bi_tan_cong=False)

    print("\n\n--- KỊCH BẢN 2: BỊ TẤN CÔNG (MITM ATTACK) ---")
    mo_phong_truyen_file(file_mau, file_dich, bi_tan_cong=True)