#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <fstream>
#include <stdexcept>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

using namespace std;
namespace py = pybind11;

typedef unsigned long long ull;
typedef long long ll;

ull mul_mod(ull a, ull b, ull m) {
    ull res = 0;
    a %= m;
    while (b > 0) {
        if (b & 1) {
            res += a;
            if (res >= m) res -= m;
        }
        a <<= 1;
        if (a >= m) a -= m;
        b >>= 1;
    }
    return res;
}

ull tinh_luy_thua(ull a, ull b, ull m) {
    ull res = 1;
    a %= m;
    while (b > 0) {
        if (b & 1) res = mul_mod(res, a, m);
        a = mul_mod(a, a, m);
        b >>= 1;
    }
    return res;
}

bool miller_rabin(ull n, int k=10) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;
    ull d = n - 1;
    int s = 0;
    while (d % 2 == 0) { d /= 2; s++; }
    for (int i = 0; i < k; i++) {
        ull a = 2 + rand() % (n - 3);
        ull x = tinh_luy_thua(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool composite = true;
        for (int r = 1; r < s; r++) {
            x = mul_mod(x, x, n);
            if (x == n - 1) { composite = false; break; }
        }
        if (composite) return false;
    }
    return true;
}

bool kiem_tra_so_nguyen_to(ull n) {
    return miller_rabin(n);
}

ull gcd(ull a, ull b) { return b == 0 ? a : gcd(b, a % b); }

ull pollard_rho(ull n) {
    if (n % 2 == 0) return 2;
    ull x = 2, y = 2, d = 1, c = 1;
    auto f = [&](ull x, ull n, ull c) { return (mul_mod(x, x, n) + c) % n; };
    while (d == 1) {
        x = f(x, n, c);
        y = f(f(y, n, c), n, c);
        d = gcd(x > y ? x - y : y - x, n);
        if (d == n) {
            x = rand() % (n - 2) + 2; y = x;
            c = rand() % (n - 1) + 1; d = 1;
        }
    }
    return d;
}

void factorize(ull n, vector<ull>& factors) {
    if (n == 1) return;
    if (miller_rabin(n, 10)) { factors.push_back(n); return; }
    ull divisor = pollard_rho(n);
    factorize(divisor, factors);
    factorize(n / divisor, factors);
}

bool kiem_tra_can_nguyen_thuy(ull a, ull q) {
    if (a <= 1 || a >= q) return false;
    ull phi = q - 1;
    vector<ull> factors;
    factorize(phi, factors);
    sort(factors.begin(), factors.end());
    factors.erase(unique(factors.begin(), factors.end()), factors.end());

    for (ull f : factors) {
        if (tinh_luy_thua(a, phi / f, q) == 1) return false;
    }
    return true;
}

ll nghich_dao_modulo(ll a, ll m) {
    ll m0 = m, t, q;
    ll x0 = 0, x1 = 1;
    if (m == 1) return 0;
    while (a > 1) {
        q = a / m;
        t = m;
        m = a % m, a = t;
        t = x0;
        x0 = x1 - q * x0;
        x1 = t;
    }
    if (x1 < 0) x1 += m0;
    return x1;
}

ull py_tao_khoa(ull q, ull a, ull XA) {
    return tinh_luy_thua(a, XA, q);
}

const string ky_tu_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

string ma_hoa_base64(const string &dau_vao) {
    string dau_ra;
    int gia_tri = 0, bit_du = -6;
    for (unsigned char c : dau_vao) {
        gia_tri = (gia_tri << 8) + c;
        bit_du += 8;
        while (bit_du >= 0) {
            dau_ra.push_back(ky_tu_base64[(gia_tri >> bit_du) & 0x3F]);
            bit_du -= 6;
        }
    }
    if (bit_du > -6) dau_ra.push_back(ky_tu_base64[((gia_tri << 8) >> (bit_du + 8)) & 0x3F]);
    while (dau_ra.size() % 4) dau_ra.push_back('=');
    return dau_ra;
}

string giai_ma_base64(const string &dau_vao) {
    string dau_ra;
    int gia_tri = 0, bit_du = -8;
    for (unsigned char c : dau_vao) {
        if (c == '=') break;
        int vi_tri = ky_tu_base64.find(c);
        if (vi_tri == string::npos) continue;
        gia_tri = (gia_tri << 6) + vi_tri;
        bit_du += 6;
        if (bit_du >= 0) {
            dau_ra.push_back(char((gia_tri >> bit_du) & 0xFF));
            bit_du -= 8;
        }
    }
    return dau_ra;
}

string ma_hoa_van_ban(ull q, ull a, ull YA, string ban_ro, ull k) {
    string chuoi_ma_hoa_tho = "";
    for (int i = 0; i < ban_ro.length(); i++) {
        unsigned char b = ban_ro[i];
        if (b >= q) throw std::invalid_argument("Ma ky tu lon hon q");
        ull C1 = tinh_luy_thua(a, k, q);
        ull K = tinh_luy_thua(YA, k, q);
        ull C2 = mul_mod(K, b, q);
        chuoi_ma_hoa_tho += to_string(C1) + "_" + to_string(C2);
        if (i < ban_ro.length() - 1) chuoi_ma_hoa_tho += "-";
    }
    return ma_hoa_base64(chuoi_ma_hoa_tho);
}

string giai_ma_van_ban(ull q, ull XA, string chuoi_b64) {
    string chuoi_ma_hoa_tho = giai_ma_base64(chuoi_b64);
    string ban_giai_ma = "";
    string cap_gia_tri_hien_tai = "";

    for (int i = 0; i <= chuoi_ma_hoa_tho.length(); i++) {
        if (i == chuoi_ma_hoa_tho.length() || chuoi_ma_hoa_tho[i] == '-') {
            if (cap_gia_tri_hien_tai != "") {
                int vi_tri = cap_gia_tri_hien_tai.find('_');
                ull C1 = stoull(cap_gia_tri_hien_tai.substr(0, vi_tri));
                ull C2 = stoull(cap_gia_tri_hien_tai.substr(vi_tri + 1));

                ull K = tinh_luy_thua(C1, XA, q);
                ull K_nghich_dao = nghich_dao_modulo(K, q);
                char M = (char)mul_mod(C2, K_nghich_dao, q);
                ban_giai_ma += M;
                cap_gia_tri_hien_tai = "";
            }
        } else {
            cap_gia_tri_hien_tai += chuoi_ma_hoa_tho[i];
        }
    }
    return ban_giai_ma;
}

ull bam_tep_tin(string duong_dan_tep) {
    ifstream tep(duong_dan_tep.c_str(), ios::binary);
    if (!tep) return 0;
    ull ma_bam = 14695981039346656037ULL;
    char c;
    while (tep.get(c)) {
        ma_bam ^= (unsigned char)c;
        ma_bam *= 1099511628211ULL;
    }
    tep.close();
    return ma_bam;
}

py::tuple py_ky_tep_tin(ull q, ull a, ull XA, ull k, string duong_dan_tep) {
    ull m = bam_tep_tin(duong_dan_tep);
    ull r = tinh_luy_thua(a, k, q);
    ull k_nghich_dao = nghich_dao_modulo(k, q - 1);

    ll tu_so = (ll)(m % (q - 1)) - (ll)mul_mod(XA, r, q - 1);
    tu_so %= (ll)(q - 1);
    if (tu_so < 0) tu_so += (q - 1);

    ull s = mul_mod((ull)tu_so, k_nghich_dao, q - 1);
    return py::make_tuple(r, s, m);
}

string xac_minh_chu_ky_chi_tiet(ull q, ull a, ull YA, ull r, ull s, ull m_goc, string duong_dan_tep) {
    if (r <= 0 || r >= q || s < 0 || s >= q - 1) return "SAI_DINH_DANG";
    ull m_hien_tai = bam_tep_tin(duong_dan_tep);

    ull v1_phan_1 = tinh_luy_thua(YA, r, q);
    ull v1_phan_2 = tinh_luy_thua(r, s, q);
    ull v1 = mul_mod(v1_phan_1, v1_phan_2, q);
    ull v2_goc = tinh_luy_thua(a, m_goc % (q - 1), q);

    bool tep_bi_sua = (m_hien_tai != m_goc);
    bool chu_ky_bi_sua = (v1 != v2_goc);

    if (!tep_bi_sua && !chu_ky_bi_sua) return "HOP_LE";
    else if (tep_bi_sua && !chu_ky_bi_sua) return "TEP_BI_SUA_DOI";
    else if (!tep_bi_sua && chu_ky_bi_sua) return "CHU_KY_BI_SUA_DOI";
    else return "CA_HAI_BI_SUA_DOI";
}

PYBIND11_MODULE(elgamal_core, m) {
    m.doc() = "Thu vien C++ ElGamal ho tro 64-bit";

    m.def("kiem_tra_so_nguyen_to", &kiem_tra_so_nguyen_to, "Kiem tra so nguyen to 64-bit");
    m.def("kiem_tra_can_nguyen_thuy", &kiem_tra_can_nguyen_thuy, "Kiem tra can nguyen thuy 64-bit");
    m.def("tinh_luy_thua", &tinh_luy_thua, "Tinh luy thua module 64-bit");
    m.def("tao_khoa", &py_tao_khoa, "Tao khoa cong khai YA");
    m.def("ma_hoa_van_ban", &ma_hoa_van_ban, "Ma hoa van ban thanh Base64");
    m.def("giai_ma_van_ban", &giai_ma_van_ban, "Giai ma van ban tu Base64");
    m.def("ky_tep_tin", &py_ky_tep_tin, "Ky so len file tra ve (r, s, m)");
    m.def("xac_minh_chu_ky_chi_tiet", &xac_minh_chu_ky_chi_tiet, "Xac minh va tra ve chi tiet loi");
}