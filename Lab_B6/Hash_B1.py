import hashlib

def tao_ma_bam(chuoi_dau_vao: str):
    du_lieu_byte = chuoi_dau_vao.encode('utf-8')
    
    ma_bam_sha256 = hashlib.sha256(du_lieu_byte).hexdigest()
    ma_bam_sha512 = hashlib.sha512(du_lieu_byte).hexdigest()
    
    return ma_bam_sha256, ma_bam_sha512

def thuc_hanh_bam_du_lieu():
    du_lieu_goc = "Xin chao Blue"
    print(f"--- Du lieu goc: '{du_lieu_goc}' ---")
    goc_256, goc_512 = tao_ma_bam(du_lieu_goc)
    print(f"SHA-256: {goc_256}")
    print(f"SHA-512: {goc_512}\n")
    
    du_lieu_da_sua = "xin chao Blue" 
    print(f"--- Du lieu da sua: '{du_lieu_da_sua}' ---")
    sua_256, sua_512 = tao_ma_bam(du_lieu_da_sua)
    print(f"SHA-256: {sua_256}")
    print(f"SHA-512: {sua_512}")

if __name__ == "__main__":
    thuc_hanh_bam_du_lieu()