import socket
import struct
import time
import tkinter as tk
from tkinter import messagebox
from aes_utils import encrypt_aes_cbc

# Cấu hình cổng và IP theo yêu cầu Lab 6.2
KEY_PORT = 5001
DATA_PORT = 5000
DEFAULT_IP = "172.20.10.3"

class SenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AES Sender - GUI Edition")
        self.root.geometry("500x450")
        self.root.configure(bg="#2c3e50")

        # Giao diện người dùng
        tk.Label(root, text="HỆ THỐNG GỬI AES 2 KÊNH", font=("Arial", 14, "bold"), bg="#2c3e50", fg="white").pack(pady=15)
        
        tk.Label(root, text="Địa chỉ IP Máy Nhận:", bg="#2c3e50", fg="#bdc3c7").pack()
        self.ip_entry = tk.Entry(root, width=30, justify='center', font=("Arial", 11))
        self.ip_entry.insert(0, DEFAULT_IP)
        self.ip_entry.pack(pady=5)

        tk.Label(root, text="Nội dung thông điệp:", bg="#2c3e50", fg="#bdc3c7").pack()
        self.msg_text = tk.Text(root, height=8, width=50, font=("Segoe UI", 10))
        self.msg_text.pack(pady=10, padx=20)

        # Nút gửi dữ liệu
        self.send_btn = tk.Button(root, text="MÃ HÓA & GỬI DỮ LIỆU", command=self.send_data, 
                                  bg="#e67e22", fg="white", font=("Arial", 10, "bold"), 
                                  padx=40, pady=12, cursor="hand2")
        self.send_btn.pack(pady=15)

    def send_data(self):
        target_ip = self.ip_entry.get()
        message = self.msg_text.get("1.0", tk.END).strip()

        if not message:
            messagebox.showwarning("Thông báo", "Vui lòng nhập nội dung tin nhắn.")
            return

        try:
            # Bước 1: Mã hóa dữ liệu
            key, iv, ciphertext = encrypt_aes_cbc(message)

            # Bước 2: Gửi Khóa và IV qua Kênh Khóa (Cổng 5001)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_key:
                s_key.settimeout(10.0) # Tăng timeout lên 10 giây để tránh lỗi mạng
                s_key.connect((target_ip, KEY_PORT))
                s_key.sendall(key + iv)
            
            # Nghỉ 0.5 giây để máy nhận kịp chuyển sang lắng nghe cổng dữ liệu
            time.sleep(0.5)

            # Bước 3: Gửi Bản mã qua Kênh Dữ liệu (Cổng 5000)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_data:
                s_data.settimeout(10.0)
                s_data.connect((target_ip, DATA_PORT))
                # Gửi Header độ dài 4 byte (Network byte order) trước ciphertext
                header = struct.pack('!I', len(ciphertext))
                s_data.sendall(header + ciphertext)

            messagebox.showinfo("Thành công", f"Dữ liệu đã được gửi an toàn tới {target_ip}")
        except socket.timeout:
            messagebox.showerror("Lỗi Timeout", "Hết thời gian chờ kết nối. Vui lòng kiểm tra IP và Tường lửa.")
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới máy nhận: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SenderApp(root)
    root.mainloop()