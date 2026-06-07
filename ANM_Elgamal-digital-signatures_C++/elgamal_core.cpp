#include <iostream>
#include <string>
#include <algorithm>
#include <math.h>
#include <fstream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

using namespace std;
namespace py = pybind11;

// CAC HAM TOAN HOC CO BAN
bool kiem_tra_so_nguyen_to(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i <= sqrt(n); i = i + 6)
        if (n % i == 0 || n % (i + 2) == 0) return false;
    return true;
}

int ucln(int a, int b) {
    if (b == 0) return a;
    return ucln(b, a % b);
}

string thap_phan_sang_nhi_phan(long long n) {
    if (n == 0) return "0";
    string chuoi_nhi_phan = "";
    while (n > 0) {
        chuoi_nhi_phan = to_string(n % 2) + chuoi_nhi_phan;
        n = n / 2;
    }
    return chuoi_nhi_phan;
}

int tinh_luy_thua(int a, long long b, int n) {
    string b_nhi_phan = thap_phan_sang_nhi_phan(b);
    int k = b_nhi_phan.size() - 1;
    long long f = 1;
    for(int i = 0; i <= k; i++){
        f = (f * f) % n;
        if (b_nhi_phan[i] == '1'){
            f = (f * a) % n;
        }
    }
    return (int)f;
}

int nghich_dao_modulo(int a, int m) {
    int m0 = m, t, q;
    int x0 = 0, x1 = 1;
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

bool kiem_tra_can_nguyen_thuy(int a, int q) {
    if (a <= 1 || a >= q) return false;
    int n = q - 1;
    int tam = n;
    for (int i = 2; i <= sqrt(tam); i++) {
        if (tam % i == 0) {
            if (tinh_luy_thua(a, n / i, q) == 1) return false;
            while (tam % i == 0) tam /= i;
        }
    }
    if (tam > 1) {
        if (tinh_luy_thua(a, n / tam, q) == 1) return false;
    }
    return true;
}

void tao_khoa_elgamal(int q, int a, int XA, int &YA) {
    YA = tinh_luy_thua(a, XA, q);
}

// MA HOA & GIAI MA VAN BAN
void ma_hoa_elgamal(int q, int a, int YA, int M, int k, int &C1, int &C2) {
    int K = tinh_luy_thua(YA, k, q);
    C1 = tinh_luy_thua(a, k, q);
    C2 = (1LL * K * M) % q;
}

int giai_ma_elgamal(int q, int XA, int C1, int C2) {
    int K = tinh_luy_thua(C1, XA, q);
    int K_nghich_dao = nghich_dao_modulo(K, q);
    return (1LL * C2 * K_nghich_dao) % q;
}

const string ky_tu_base64 =
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "abcdefghijklmnopqrstuvwxyz"
             "0123456789+/";

string ma_hoa_base64(const string &dau_vao) {
    string dau_ra;
    int gia_tri = 0, bit_du = -6;
    for (int i = 0; i < dau_vao.length(); i++) {
        unsigned char c = dau_vao[i];
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
    for (int i = 0; i < dau_vao.length(); i++) {
        unsigned char c = dau_vao[i];
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

string ma_hoa_van_ban(int q, int a, int YA, string ban_ro, int k) {
    string chuoi_ma_hoa_tho = "";
    for (int i = 0; i < ban_ro.length(); i++) {
        unsigned char b = ban_ro[i];
        if (b >= q) {
            throw std::invalid_argument("Ma ky tu lon hon q");
        }
        int c1, c2;
        ma_hoa_elgamal(q, a, YA, b, k, c1, c2);
        chuoi_ma_hoa_tho += to_string(c1) + "_" + to_string(c2);
        if (i < ban_ro.length() - 1) chuoi_ma_hoa_tho += "-";
    }
    return ma_hoa_base64(chuoi_ma_hoa_tho);
}

string giai_ma_van_ban(int q, int XA, string chuoi_b64) {
    string chuoi_ma_hoa_tho = giai_ma_base64(chuoi_b64);
    string ban_giai_ma = "";
    string cap_gia_tri_hien_tai = "";

    for (int i = 0; i <= chuoi_ma_hoa_tho.length(); i++) {
        if (i == chuoi_ma_hoa_tho.length() || chuoi_ma_hoa_tho[i] == '-') {
            if (cap_gia_tri_hien_tai != "") {
                int vi_tri_gach_duoi = cap_gia_tri_hien_tai.find('_');
                int c1 = stoi(cap_gia_tri_hien_tai.substr(0, vi_tri_gach_duoi));
                int c2 = stoi(cap_gia_tri_hien_tai.substr(vi_tri_gach_duoi + 1));

                char M = (char)giai_ma_elgamal(q, XA, c1, c2);
                ban_giai_ma += M;
                cap_gia_tri_hien_tai = "";
            }
        } else {
            cap_gia_tri_hien_tai += chuoi_ma_hoa_tho[i];
        }
    }
    return ban_giai_ma;
}

// CHU KY SO DIEN TU TREN TEP TIN
long long bam_tep_tin(string duong_dan_tep) {
    ifstream tep(duong_dan_tep.c_str(), ios::binary);
    if (!tep) return 0;
    unsigned int ma_bam = 2166136261u;
    char c;
    while (tep.get(c)) {
        ma_bam ^= (unsigned char)c;
        ma_bam *= 16777619;
    }
    tep.close();
    return (long long)ma_bam;
}

void ky_tep_tin(int q, int a, int XA, int k, string duong_dan_tep, int &r, int &s, long long &m) {
    if (ucln(k, q - 1) != 1) return;
    m = bam_tep_tin(duong_dan_tep);
    r = tinh_luy_thua(a, k, q);

    int k_nghich_dao = nghich_dao_modulo(k, q - 1);
    long long tam = (m - (1LL * XA * r)) % (q - 1);
    if (tam < 0) tam += (q - 1);

    s = (tam * k_nghich_dao) % (q - 1);
    if (s < 0) s += (q - 1);
}

bool xac_minh_chu_ky(int q, int a, int YA, int r, int s, string duong_dan_tep) {
    if (r <= 0 || r >= q || s < 0 || s >= q - 1) return false;
    long long m = bam_tep_tin(duong_dan_tep);
    long long v1_phan_1 = tinh_luy_thua(YA, r, q);
    long long v1_phan_2 = tinh_luy_thua(r, s, q);
    long long v1 = (v1_phan_1 * v1_phan_2) % q;

    long long v2 = tinh_luy_thua(a, m % (q - 1), q);
    return v1 == v2;
}

string xac_minh_chu_ky_chi_tiet(int q, int a, int YA, int r, int s, long long m_goc, string duong_dan_tep) {
    if (r <= 0 || r >= q || s < 0 || s >= q - 1) {
        return "SAI_DINH_DANG";
    }

    long long m_hien_tai = bam_tep_tin(duong_dan_tep);

    long long v1_phan_1 = tinh_luy_thua(YA, r, q);
    long long v1_phan_2 = tinh_luy_thua(r, s, q);
    long long v1 = (v1_phan_1 * v1_phan_2) % q;

    long long v2_goc = tinh_luy_thua(a, m_goc % (q - 1), q);

    bool tep_bi_sua = (m_hien_tai != m_goc);
    bool chu_ky_bi_sua = (v1 != v2_goc);

    if (!tep_bi_sua && !chu_ky_bi_sua) {
        return "HOP_LE";
    } else if (tep_bi_sua && !chu_ky_bi_sua) {
        return "TEP_BI_SUA_DOI";
    } else if (!tep_bi_sua && chu_ky_bi_sua) {
        return "CHU_KY_BI_SUA_DOI";
    } else {
        return "CA_HAI_BI_SUA_DOI";
    }
}

int py_tao_khoa(int q, int a, int XA) {
    int YA;
    tao_khoa_elgamal(q, a, XA, YA);
    return YA;
}

py::tuple py_ky_tep_tin(int q, int a, int XA, int k, std::string duong_dan_tep) {
    int r = 0, s = 0;
    long long m = 0;
    ky_tep_tin(q, a, XA, k, duong_dan_tep, r, s, m);
    return py::make_tuple(r, s, m);
}

PYBIND11_MODULE(elgamal_core, m) {
    m.doc() = "Thu vien C++ ElGamal duoc boc bang pybind11";

    m.def("kiem_tra_so_nguyen_to", &kiem_tra_so_nguyen_to, "Kiem tra so nguyen to");
    m.def("kiem_tra_can_nguyen_thuy", &kiem_tra_can_nguyen_thuy, "Kiem tra can nguyen thuy");
    m.def("tinh_luy_thua", &tinh_luy_thua, "Tinh luy thua bieu dien nhi phan");
    m.def("tao_khoa", &py_tao_khoa, "Tao khoa cong khai YA");
    m.def("ma_hoa_van_ban", &ma_hoa_van_ban, "Ma hoa van ban thanh Base64");
    m.def("giai_ma_van_ban", &giai_ma_van_ban, "Giai ma van ban tu Base64");
    m.def("ky_tep_tin", &py_ky_tep_tin, "Ky so len file tra ve (r, s, m)");
    m.def("xac_minh_chu_ky", &xac_minh_chu_ky, "Xac minh chu ky file tra ve dung/sai");
    m.def("xac_minh_chu_ky_chi_tiet", &xac_minh_chu_ky_chi_tiet, "Xac minh va tra ve chi tiet loi");
}