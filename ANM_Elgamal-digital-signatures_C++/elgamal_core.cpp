#include <iostream>
#include <string>
#include <algorithm>
#include <math.h>
#include <fstream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> 

using namespace std;
namespace py = pybind11;

bool isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i <= sqrt(n); i = i + 6)
        if (n % i == 0 || n % (i + 2) == 0) return false;
    return true;
}

int gcd(int a, int b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}

string decimalToBinary(long long n) {
    if (n == 0) return "0";
    string binary = "";
    while (n > 0) {
        binary = to_string(n % 2) + binary;  
        n = n / 2;
    }
    return binary;
}

int calcExponent(int a, long long b, int n) {
    string b_binary = decimalToBinary(b);
    int k = b_binary.size() - 1;
    long long f = 1; 
    for(int i = 0; i <= k; i++){
        f = (f * f) % n;
        if (b_binary[i] == '1'){
            f = (f * a) % n;
        }                                                                                                                                                                                                                                                             
    }    
    return (int)f;                                                                                                      
}

int modInverse(int a, int m) {
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

bool isPrimitiveRoot(int a, int q) {
    if (a <= 1 || a >= q) return false;
    int n = q - 1;
    int temp = n;
    for (int i = 2; i <= sqrt(temp); i++) {
        if (temp % i == 0) {
            if (calcExponent(a, n / i, q) == 1) return false;
            while (temp % i == 0) temp /= i;
        }
    }
    if (temp > 1) {
        if (calcExponent(a, n / temp, q) == 1) return false;
    }
    return true;
}

void generateKeys(int q, int a, int XA, int &YA) {
    YA = calcExponent(a, XA, q);
}

void encryptElgamal(int q, int a, int YA, int M, int k, int &C1, int &C2) {
    int K = calcExponent(YA, k, q);
    C1 = calcExponent(a, k, q);     
    C2 = (1LL * K * M) % q;
}

int decryptElgamal(int q, int XA, int C1, int C2) {
    int K = calcExponent(C1, XA, q);   
    int K_inv = modInverse(K, q);       
    return (1LL * C2 * K_inv) % q;     
}

const string base64_chars = 
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "abcdefghijklmnopqrstuvwxyz"
             "0123456789+/";

string base64_encode(const string &in) {
    string out;
    int val = 0, valb = -6;
    for (int i = 0; i < in.length(); i++) {
        unsigned char c = in[i];
        val = (val << 8) + c;
        valb += 8;
        while (valb >= 0) {
            out.push_back(base64_chars[(val >> valb) & 0x3F]);
            valb -= 6;
        }
    }
    if (valb > -6) out.push_back(base64_chars[((val << 8) >> (valb + 8)) & 0x3F]);
    while (out.size() % 4) out.push_back('=');
    return out;
}

string base64_decode(const string &in) {
    string out;
    int val = 0, valb = -8;
    for (int i = 0; i < in.length(); i++) {
        unsigned char c = in[i];
        if (c == '=') break;
        int index = base64_chars.find(c);
        if (index == string::npos) continue;
        val = (val << 6) + index;
        valb += 6;
        if (valb >= 0) {
            out.push_back(char((val >> valb) & 0xFF));
            valb -= 8;
        }
    }
    return out;
}

string encrypt_text(int q, int a, int YA, string plain_text, int k) {
    string raw_cipher_string = "";
    for (int i = 0; i < plain_text.length(); i++) {
        unsigned char b = plain_text[i];
        if (b >= q) {
            throw std::invalid_argument("Ma ky tu lon hon q");
        }
        int c1, c2;
        encryptElgamal(q, a, YA, b, k, c1, c2);
        raw_cipher_string += to_string(c1) + "_" + to_string(c2);
        if (i < plain_text.length() - 1) raw_cipher_string += "-";
    }
    return base64_encode(raw_cipher_string);
}

string decrypt_text(int q, int XA, string b64_encoded) {
    string raw_cipher_string = base64_decode(b64_encoded);
    string decrypted_text = "";
    string current_pair = "";
    
    for (int i = 0; i <= raw_cipher_string.length(); i++) {
        if (i == raw_cipher_string.length() || raw_cipher_string[i] == '-') {
            if (current_pair != "") {
                int underscore_pos = current_pair.find('_');
                int c1 = stoi(current_pair.substr(0, underscore_pos));
                int c2 = stoi(current_pair.substr(underscore_pos + 1));
                
                char M = (char)decryptElgamal(q, XA, c1, c2);
                decrypted_text += M;
                current_pair = "";
            }
        } else {
            current_pair += raw_cipher_string[i];
        }
    }
    return decrypted_text;
}

long long hash_file(string filepath) {
    ifstream file(filepath.c_str(), ios::binary);
    if (!file) return 0;
    unsigned int hash = 2166136261u;
    char c;
    while (file.get(c)) {
        hash ^= (unsigned char)c;
        hash *= 16777619;
    }
    file.close();
    return (long long)hash;
}

void sign_file(int q, int a, int XA, int k, string filepath, int &r, int &s) {
    if (gcd(k, q - 1) != 1) return;
    long long m = hash_file(filepath);
    r = calcExponent(a, k, q);
    int k_inv = modInverse(k, q - 1);
    long long temp = (m - (1LL * XA * r)) % (q - 1);
    if (temp < 0) temp += (q - 1);
    s = (temp * k_inv) % (q - 1);
    if (s < 0) s += (q - 1);
}

bool verify_signature(int q, int a, int YA, int r, int s, string filepath) {
    if (r <= 0 || r >= q || s < 0 || s >= q - 1) return false;
    long long m = hash_file(filepath);
    long long v1_part1 = calcExponent(YA, r, q);
    long long v1_part2 = calcExponent(r, s, q);
    long long v1 = (v1_part1 * v1_part2) % q;
    long long v2 = calcExponent(a, m % (q - 1), q);
    return v1 == v2;
}

int py_generate_keys(int q, int a, int XA) {
    int YA;
    generateKeys(q, a, XA, YA);
    return YA;
}

py::tuple py_sign_file(int q, int a, int XA, int k, std::string filepath) {
    int r = 0, s = 0;
    sign_file(q, a, XA, k, filepath, r, s);
    return py::make_tuple(r, s);
}

PYBIND11_MODULE(elgamal_core, m) {
    m.doc() = "Thu vien C++ ElGamal duoc boc bang pybind11";

    m.def("is_prime", &isPrime, "Kiem tra so nguyen to");
    m.def("is_primitive_root", &isPrimitiveRoot, "Kiem tra can nguyen thuy");
    m.def("calc_exponent", &calcExponent, "Tinh luy thua bieu dien nhi phan");
    m.def("generate_keys", &py_generate_keys, "Tao khoa cong khai YA");
    m.def("encrypt_text", &encrypt_text, "Ma hoa van ban thanh Base64");
    m.def("decrypt_text", &decrypt_text, "Giai ma van ban tu Base64");
    m.def("sign_file", &py_sign_file, "Ky so len file");
    m.def("verify_signature", &verify_signature, "Xac minh chu ky file");
}
