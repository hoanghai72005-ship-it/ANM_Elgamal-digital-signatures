import math
import base64
import hashlib


def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0: return False
    return True


def decimal_to_binary(n):
    if n == 0: return "0"
    binary = ""
    while n > 0:
        binary = str(n % 2) + binary
        n = n // 2
    return binary


def calc_exponent(a, b, n):
    b_binary = decimal_to_binary(b)
    f = 1
    for bit in b_binary:
        f = (f * f) % n
        if bit == '1': f = (f * a) % n
    return f


def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1: return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += m0
    return x1


def is_primitive_root(a, q):
    if a <= 1 or a >= q: return False
    n = q - 1
    temp = n
    i = 2
    while i * i <= temp:
        if temp % i == 0:
            if calc_exponent(a, n // i, q) == 1: return False
            while temp % i == 0: temp //= i
        i += 1
    if temp > 1:
        if calc_exponent(a, n // temp, q) == 1: return False
    return True


def generate_keys(q, a, XA):
    return calc_exponent(a, XA, q)


# MÃ HÓA & GIẢI MÃ VĂN BẢN
def encrypt_elgamal(q, a, YA, M, k):
    K = calc_exponent(YA, k, q)
    c1 = calc_exponent(a, k, q)
    c2 = (K * M) % q
    return c1, c2


def decrypt_elgamal(q, XA, c1, c2):
    K = calc_exponent(c1, XA, q)
    K_inv = mod_inverse(K, q)
    return (c2 * K_inv) % q


def encrypt_text(q, a, YA, plain_text, k):
    bytes_data = plain_text.encode('utf-8')
    encrypted_pairs = []
    for b in bytes_data:
        if b >= q:
            raise ValueError(f"Mã ký tự ({b}) lớn hơn hoặc bằng q ({q}). Vui lòng chọn q > 255.")
        c1, c2 = encrypt_elgamal(q, a, YA, b, k)
        encrypted_pairs.append(f"{c1}_{c2}")
    raw_cipher_string = "-".join(encrypted_pairs)
    return base64.b64encode(raw_cipher_string.encode('ascii')).decode('ascii')


def decrypt_text(q, XA, b64_encoded):
    raw_cipher_string = base64.b64decode(b64_encoded).decode('ascii')
    pairs = raw_cipher_string.split('-')
    decrypted_bytes = bytearray()
    for pair in pairs:
        if not pair: continue
        c1_str, c2_str = pair.split('_')
        M = decrypt_elgamal(q, XA, int(c1_str), int(c2_str))
        decrypted_bytes.append(M)
    return decrypted_bytes.decode('utf-8')


# CHỮ KÝ SỐ ĐIỆN TỬ TRÊN FILE
def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return int(sha256.hexdigest(), 16)


def sign_file(q, a, XA, k, filepath):
    if math.gcd(k, q - 1) != 1:
        raise ValueError(f"Số k = {k} không hợp lệ. gcd(k, q-1) phải bằng 1.")

    m = hash_file(filepath)
    r = calc_exponent(a, k, q)

    k_inv = mod_inverse(k, q - 1)
    s = ((m - XA * r) * k_inv) % (q - 1)

    if s < 0:
        s += (q - 1)

    return r, s


def verify_signature(q, a, YA, r, s, filepath):
    if not (0 < r < q) or not (0 <= s < q - 1):
        return False

    m = hash_file(filepath)
    v1 = (calc_exponent(YA, r, q) * calc_exponent(r, s, q)) % q
    v2 = calc_exponent(a, m, q)

    return v1 == v2