#include <iostream>
#include <string>
#include <algorithm>
#include <math.h>

using namespace std;

bool isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i <= sqrt(n); i = i + 6)
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
    return true;
}

bool isPrimitiveRoot(int a, int q) {
    if (a <= 1 || a >= q) return false;

    int n = q - 1;
    int temp = n;

    for (int i = 2; i <= sqrt(temp); i++) {
        if (temp % i == 0) {
            if (calcExponent(a, n / i, q) == 1) {
                return false;
            }
            while (temp % i == 0) {
                temp /= i;
            }
        }
    }
    if (temp > 1) {
        if (calcExponent(a, n / temp, q) == 1) {
            return false;
        }
    }
    return true;
}

string decimalToBinary(int n) {
    if (n == 0) return "0";
    string binary = "";
    while (n > 0) {
        binary = to_string(n % 2) + binary;  
        n = n / 2;
    }
    return binary;
}

int calcExponent(int a, int b, int n){
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

int main() {
    int q, a, XA, k, M, YA, C1, C2;

    while (true) {
        cout << "q = "; cin >> q;
        if (isPrime(q)) break;
        cout << "Loi: q phai la so nguyen to. Vui long nhap lai!" << endl;
    }
	
	while (true) {
        cout << "a = "; cin >> a;
        if (isPrimitiveRoot(a, q)) break;
        cout << "Loi: a phai la can nguyen thuy cua " << q << ". Vui long nhap lai!" << endl;
    }
    
    cout << "XA (XA < q - 1) = "; 	cin >> XA;

    generateKeys(q, a, XA, YA);
    cout << "Khoa cong khai Kp = {" << q << ", " << a << ", " << YA << "}" << endl;
    cout << "Khoa bi mat Ks = {" << XA << "}" << endl;

    do {
        cout << "M (0 < M < " << q << ") =  "; 
        cin >> M;
        if (M <= 0 || M >= q) {
            cout << "Loi: Thong diep M phai thoa man 0 < M < q. Vui long nhap lai!" << endl;
        }
    } while (M <= 0 || M >= q);
    
    cout << "k (k < q) = "; cin >> k;
    encryptElgamal(q, a, YA, M, k, C1, C2);
    cout << "Ban ma gui di: {C1, C2} = {" << C1 << ", " << C2 << "}" << endl;

    int decryptedM = decryptElgamal(q, XA, C1, C2);
    cout << "Ket qua giai ma: M = " << decryptedM << endl;

    return 0;
}
