import math
import base64
import hashlib


# CAC HAM TOAN HOC CO BAN
def la_so_nguyen_to(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0: return False
    return True


def thap_phan_sang_nhi_phan(n):
    if n == 0: return "0"
    nhi_phan = ""
    while n > 0:
        nhi_phan = str(n % 2) + nhi_phan
        n = n // 2
    return nhi_phan


def tinh_luy_thua_module(a, b, n):
    nhi_phan_b = thap_phan_sang_nhi_phan(b)
    f = 1
    for bit in nhi_phan_b:
        f = (f * f) % n
        if bit == '1': f = (f * a) % n
    return f


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


def tao_khoa(q, a, XA):
    return tinh_luy_thua_module(a, XA, q)


# MA HOA & GIAI MA VAN BAN
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
            raise ValueError(f"Mã ký tự ({b}) lớn hơn hoặc bằng q ({q}). Vui lòng chọn q > 255.")
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


# CHU KY SO DIEN TU TREN FILE
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