import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Kích thước khối AES cố định là 16 bytes
BLOCK_SIZE = 16

def encrypt_aes_cbc(plain_text: str):
    # Khởi tạo AES-256 (Khóa 32 bytes) và IV (16 bytes)
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Thực hiện đệm PKCS#7 và mã hóa
    ciphertext = cipher.encrypt(pad(plain_text.encode('utf-8'), BLOCK_SIZE))
    return key, iv, ciphertext

def decrypt_aes_cbc(key: bytes, iv: bytes, ciphertext: bytes):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Giải mã và loại bỏ đệm
    return unpad(cipher.decrypt(ciphertext), BLOCK_SIZE).decode('utf-8')

def recv_exact(conn, n: int):
    """Đảm bảo nhận đủ số lượng byte yêu cầu từ Socket."""
    data = b''
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet: return None
        data += packet
    return data