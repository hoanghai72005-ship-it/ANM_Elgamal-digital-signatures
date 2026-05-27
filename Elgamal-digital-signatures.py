import math

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def decimal_to_binary(n):
    if n == 0:
        return "0"
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
        if bit == '1':
            f = (f * a) % n
    return f


def mod_inverse(a, m):
    m0 = m
    x0, x1 = 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = x0
        x0 = x1 - q * x0
        x1 = t
    if x1 < 0:
        x1 += m0
    return x1


def is_primitive_root(a, q):
    if a <= 1 or a >= q:
        return False

    n = q - 1
    temp = n

    i = 2
    while i * i <= temp:
        if temp % i == 0:
            if calc_exponent(a, n // i, q) == 1:
                return False
            while temp % i == 0:
                temp //= i
        i += 1

    if temp > 1:
        if calc_exponent(a, n // temp, q) == 1:
            return False

    return True


def generate_keys(q, a, XA):
    YA = calc_exponent(a, XA, q)
    return YA


def encrypt_elgamal(q, a, YA, M, k):
    K = calc_exponent(YA, k, q)
    C1 = calc_exponent(a, k, q)
    C2 = (K * M) % q
    return C1, C2


def decrypt_elgamal(q, XA, C1, C2):
    K = calc_exponent(C1, XA, q)
    K_inv = mod_inverse(K, q)
    return (C2 * K_inv) % q

def main():
    while True:
        try:
            q = int(input("q = "))
            if is_prime(q):
                break
            print("Loi: q phai la so nguyen to. Vui long nhap lai!")
        except ValueError:
            print("Loi: Vui long nhap mot so nguyen hợp le.")

    while True:
        try:
            a = int(input(f"a (a < {q}) = "))
            if is_primitive_root(a, q):
                break
            print(f"Loi: a phai la can nguyen thuy cua {q}. Vui long nhap lai!")
        except ValueError:
            print("Loi: Vui long nhap mot so nguyen hợp le.")

    XA = int(input(f"XA (XA < {q - 1}) = "))

    YA = generate_keys(q, a, XA)
    print(f"Khoa cong khai Kp = {{{q}, {a}, {YA}}}")
    print(f"Khoa bi mat Ks = {{{XA}}}")

    while True:
        M = int(input(f"M (0 < M < {q}) = "))
        if 0 < M < q:
            break
        print(f"Loi: Thong diep M phai thoa man 0 < M < {q}. Vui long nhap lai!")

    k = int(input(f"k (k < {q}) = "))

    C1, C2 = encrypt_elgamal(q, a, YA, M, k)
    print(f"Ban ma gui di: {{C1, C2}} = {{{C1}, {C2}}}")

    decryptedM = decrypt_elgamal(q, XA, C1, C2)
    print(f"Ket qua giai ma: M = {decryptedM}")

if __name__ == "__main__":
    main()