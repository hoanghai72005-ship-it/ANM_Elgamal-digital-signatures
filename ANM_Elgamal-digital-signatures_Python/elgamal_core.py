import math
import base64
import hashlib
import random

DANH_SACH_NGUYEN_TO_NHO = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
    157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
    239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
    421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 499, 503, 509,
    521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613,
    617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709,
    719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821,
    823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919,
    929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997
]


def la_so_nguyen_to(n, k=20):
    if n <= 1: return False
    if n in DANH_SACH_NGUYEN_TO_NHO: return True
    for p in DANH_SACH_NGUYEN_TO_NHO:
        if n % p == 0: return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = tinh_luy_thua_module(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def thap_phan_sang_nhi_phan(n):
    return bin(n)[2:]


def tinh_luy_thua_module(a, b, n):
    ket_qua = 1
    a = a % n
    while b > 0:
        if b % 2 == 1:
            ket_qua = (ket_qua * a) % n
        b //= 2
        a = (a * a) % n
    return ket_qua


def nghich_dao_module(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1: return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += m0
    return x1


def la_can_nguyen_thuy(a, q):
    if a <= 1 or a >= q: return False

    p = (q - 1) // 2
    if la_so_nguyen_to(p):
        if tinh_luy_thua_module(a, 2, q) == 1: return False
        if tinh_luy_thua_module(a, p, q) == 1: return False
        return True

    if q < 10 ** 12:
        n = q - 1
        tam = n
        i = 2
        while i * i <= tam:
            if tam % i == 0:
                if tinh_luy_thua_module(a, n // i, q) == 1: return False
                while tam % i == 0: tam //= i
            i += 1
        if tam > 1:
            if tinh_luy_thua_module(a, n // tam, q) == 1: return False
        return True

    return False


def sinh_so_nguyen_to_an_toan(bit_length):
    while True:
        p = random.getrandbits(bit_length - 1)
        p |= (1 << (bit_length - 2)) | 1

        hop_so = False
        for prime in DANH_SACH_NGUYEN_TO_NHO:
            if p % prime == 0 and p != prime:
                hop_so = True
                break
        if hop_so: continue

        if la_so_nguyen_to(p):
            q = 2 * p + 1
            # Sàng lọc nhanh số q
            for prime in DANH_SACH_NGUYEN_TO_NHO:
                if q % prime == 0 and q != prime:
                    hop_so = True
                    break
            if hop_so: continue

            if la_so_nguyen_to(q):
                return q


def tao_khoa(q, a, XA):
    return tinh_luy_thua_module(a, XA, q)


# 2. MÃ HÓA & GIẢI MÃ VĂN BẢN

def ma_hoa_elgamal(q, a, YA, M, k):
    K = tinh_luy_thua_module(YA, k, q)
    c1 = tinh_luy_thua_module(a, k, q)
    c2 = (K * M) % q
    return c1, c2


def giai_ma_elgamal(q, XA, c1, c2):
    K = tinh_luy_thua_module(c1, XA, q)
    K_nghich_dao = nghich_dao_module(K, q)
    return (c2 * K_nghich_dao) % q


def ma_hoa_van_ban(q, a, YA, ban_ro, k):
    du_lieu_byte = ban_ro.encode('utf-8')
    cac_cap_ma_hoa = []
    for b in du_lieu_byte:
        if b >= q:
            raise ValueError(f"Mã ký tự ({b}) lớn hơn hoặc bằng q ({q}). Vui lòng chọn cấu hình bit lớn hơn.")
        c1, c2 = ma_hoa_elgamal(q, a, YA, b, k)
        cac_cap_ma_hoa.append(f"{c1}_{c2}")
    chuoi_ma_hoa_tho = "-".join(cac_cap_ma_hoa)
    return base64.b64encode(chuoi_ma_hoa_tho.encode('ascii')).decode('ascii')


def giai_ma_van_ban(q, XA, chuoi_b64):
    chuoi_ma_hoa_tho = base64.b64decode(chuoi_b64).decode('ascii')
    cac_cap = chuoi_ma_hoa_tho.split('-')
    byte_giai_ma = bytearray()
    for cap in cac_cap:
        if not cap: continue
        c1_str, c2_str = cap.split('_')
        M = giai_ma_elgamal(q, XA, int(c1_str), int(c2_str))
        byte_giai_ma.append(M)
    return byte_giai_ma.decode('utf-8')


# 3. CHỮ KÝ SỐ ĐIỆN TỬ TRÊN FILE

def bam_tep(duong_dan_tep):
    sha256 = hashlib.sha256()
    with open(duong_dan_tep, 'rb') as f:
        while khoi := f.read(8192):
            sha256.update(khoi)
    return int(sha256.hexdigest(), 16)


def ky_tep(q, a, XA, k, duong_dan_tep):
    if math.gcd(k, q - 1) != 1:
        raise ValueError(f"Số k = {k} không hợp lệ. gcd(k, q-1) phải bằng 1.")

    m = bam_tep(duong_dan_tep)
    r = tinh_luy_thua_module(a, k, q)

    k_nghich_dao = nghich_dao_module(k, q - 1)
    s = ((m - XA * r) * k_nghich_dao) % (q - 1)

    if s < 0:
        s += (q - 1)

    return r, s, m


def xac_thuc_chu_ky(q, a, YA, r, s, duong_dan_tep):
    if not (0 < r < q) or not (0 <= s < q - 1):
        return False
    m = bam_tep(duong_dan_tep)
    v1 = (tinh_luy_thua_module(YA, r, q) * tinh_luy_thua_module(r, s, q)) % q
    v2 = tinh_luy_thua_module(a, m, q)
    return v1 == v2


def xac_thuc_chu_ky_chi_tiet(q, a, YA, r, s, m_goc, duong_dan_tep):
    if not (0 < r < q) or not (0 <= s < q - 1):
        return "SAI_DINH_DANG"

    m_hien_tai = bam_tep(duong_dan_tep)

    v1 = (tinh_luy_thua_module(YA, r, q) * tinh_luy_thua_module(r, s, q)) % q
    v2_goc = tinh_luy_thua_module(a, m_goc, q)

    tep_da_doi = (m_hien_tai != m_goc)
    chu_ky_da_doi = (v1 != v2_goc)

    if not tep_da_doi and not chu_ky_da_doi:
        return "HOP_LE"
    elif tep_da_doi and not chu_ky_da_doi:
        return "TEP_DA_DOI"
    elif not tep_da_doi and chu_ky_da_doi:
        return "CHU_KY_DA_DOI"
    else:
        return "CA_HAI_DA_DOI"