import math
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

import elgamal_core as core


class ElGamalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ mật mã ElGamal")
        self.root.geometry("1100x780")

        try:
            self.root.state('zoomed')
        except:
            pass

        self.BG_APP = "#F3F4F6"
        self.BG_CARD = "#FFFFFF"
        self.COLOR_BTN_PRI = "#0D6EFD"
        self.COLOR_BTN_SEC = "#198754"
        self.COLOR_BTN_DEF = "#6C757D"

        self.root.configure(bg=self.BG_APP)
        self.font_title = ("Segoe UI", 11, "bold")
        self.font_label = ("Segoe UI", 10)
        self.font_bold = ("Segoe UI", 10, "bold")

        self.q = self.a = self.XA = self.YA = None
        self.k_enc_confirmed = None
        self.k_sig_confirmed = None

        self.key_mode = tk.IntVar(value=2)

        self.build_key_generation_frame()
        self.build_tabs()
        self.toggle_key_mode()

    def style_entry(self, parent, width=25):
        return tk.Entry(parent, width=width, font=self.font_label, relief="solid", bd=1)

    def style_button(self, parent, text, color, command, width=20):
        return tk.Button(parent, text=text, font=self.font_bold, bg=color, fg="white",
                         activebackground="#212529", activeforeground="white",
                         relief="flat", cursor="hand2", width=width, pady=3, command=command)

    # ==========================================
    # PHẦN 1: KHUNG TẠO KHÓA CHUNG
    # ==========================================
    def build_key_generation_frame(self):
        self.frame_keys = tk.LabelFrame(self.root, text=" Giai đoạn sinh khóa ", font=self.font_title, bg=self.BG_CARD,
                                        padx=15, pady=5, relief="flat")
        self.frame_keys.pack(fill="x", padx=15, pady=10)

        frame_radios = tk.Frame(self.frame_keys, bg=self.BG_CARD)
        frame_radios.pack(pady=(0, 3))
        tk.Radiobutton(frame_radios, text="Tùy chọn (Nhập tay)", variable=self.key_mode, value=1,
                       command=self.toggle_key_mode, font=self.font_label, bg=self.BG_CARD).pack(side="left", padx=20)
        tk.Radiobutton(frame_radios, text="Tự động chọn", variable=self.key_mode, value=2, command=self.toggle_key_mode,
                       font=self.font_label, bg=self.BG_CARD).pack(side="left", padx=20)

        frame_inputs = tk.Frame(self.frame_keys, bg=self.BG_CARD)
        frame_inputs.pack(fill="x")

        tk.Label(frame_inputs, text="Chọn số nguyên tố q đủ lớn:", font=self.font_label, bg=self.BG_CARD).grid(row=0,
                                                                                                               column=0,
                                                                                                               sticky="w",
                                                                                                               pady=2)
        self.ent_q = self.style_entry(frame_inputs)
        self.ent_q.grid(row=0, column=1, padx=15)

        tk.Label(frame_inputs, text="Chọn a là căn nguyên thủy của q (a < q):", font=self.font_label,
                 bg=self.BG_CARD).grid(row=1, column=0, sticky="w", pady=2)
        self.ent_a = self.style_entry(frame_inputs)
        self.ent_a.grid(row=1, column=1, padx=15)

        tk.Label(frame_inputs, text="Chọn Khóa bí mật XA (XA < q - 1):", font=self.font_label, bg=self.BG_CARD).grid(
            row=2, column=0, sticky="w", pady=2)
        self.ent_x = self.style_entry(frame_inputs)
        self.ent_x.grid(row=2, column=1, padx=15)

        frame_key_btns = tk.Frame(self.frame_keys, bg=self.BG_CARD)
        frame_key_btns.pack(pady=5)
        self.btn_random_keys = self.style_button(frame_key_btns, "Tạo khóa ngẫu nhiên", self.COLOR_BTN_DEF,
                                                 self.generate_random_keys_ui)
        self.btn_random_keys.grid(row=0, column=0, padx=10)
        self.btn_confirm_keys = self.style_button(frame_key_btns, "Tính YA & Xác nhận Khóa", self.COLOR_BTN_SEC,
                                                  self.confirm_keys)
        self.btn_confirm_keys.grid(row=0, column=1, padx=10)

        self.frame_key_results = tk.Frame(self.frame_keys, bg="#E8F4F8", padx=15, pady=5)
        self.frame_key_results.pack(fill="x", pady=5)

        tk.Label(self.frame_key_results, text="Tính toán: YA = a^XA mod q =", font=self.font_label, bg="#E8F4F8").grid(
            row=0, column=0, sticky="w", pady=2)
        self.lbl_ya_res = tk.Label(self.frame_key_results, text="", font=self.font_bold, bg="#E8F4F8")
        self.lbl_ya_res.grid(row=0, column=1, sticky="w", padx=10)
        tk.Label(self.frame_key_results, text="Khóa công khai {q, a, YA}:", font=self.font_label, bg="#E8F4F8").grid(
            row=1, column=0, sticky="w", pady=2)
        self.lbl_pub_key = tk.Label(self.frame_key_results, text="", font=self.font_bold, fg="#DC3545", bg="#E8F4F8")
        self.lbl_pub_key.grid(row=1, column=1, sticky="w", padx=10)
        tk.Label(self.frame_key_results, text="Khóa bí mật {XA}:", font=self.font_label, bg="#E8F4F8").grid(row=2,
                                                                                                            column=0,
                                                                                                            sticky="w",
                                                                                                            pady=2)
        self.lbl_priv_key = tk.Label(self.frame_key_results, text="", font=self.font_bold, fg="#DC3545", bg="#E8F4F8")
        self.lbl_priv_key.grid(row=2, column=1, sticky="w", padx=10)

    # ==========================================
    # PHẦN 2: THIẾT KẾ CÁC TABS
    # ==========================================
    def build_tabs(self):
        self.notebook = ttk.Notebook(self.root)

        self.tab_crypto = tk.Frame(self.notebook, bg=self.BG_APP)
        self.notebook.add(self.tab_crypto, text=" Mã hóa Chuỗi Text ")
        self.build_crypto_ui(self.tab_crypto)

        self.tab_signature = tk.Frame(self.notebook, bg=self.BG_APP)
        self.notebook.add(self.tab_signature, text=" Chữ ký số ElGamal ")
        self.build_signature_ui(self.tab_signature)

    # --- UI TAB 1: MÃ HÓA ---
    def build_crypto_ui(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

        # Cột Trái: Mã Hóa
        frame_left = tk.LabelFrame(parent, text=" Mã hóa ", font=self.font_title, bg=self.BG_CARD, padx=15, pady=5,
                                   relief="flat")
        frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        tk.Label(frame_left, text="Bản rõ:", font=self.font_label, bg=self.BG_CARD).pack(anchor="w")
        self.txt_plain = tk.Text(frame_left, height=2, font=self.font_label, relief="solid", bd=1)
        self.txt_plain.pack(fill="x", pady=(2, 5))

        self.k_mode_enc = tk.IntVar(value=2)
        frame_k = tk.Frame(frame_left, bg=self.BG_CARD)
        frame_k.pack(fill="x", pady=2)
        tk.Radiobutton(frame_k, text="Tùy chọn k", variable=self.k_mode_enc, value=1, command=self.toggle_k_enc,
                       font=self.font_label, bg=self.BG_CARD).pack(side="left")
        tk.Radiobutton(frame_k, text="Tự động chọn k", variable=self.k_mode_enc, value=2, command=self.toggle_k_enc,
                       font=self.font_label, bg=self.BG_CARD).pack(side="left", padx=15)

        frame_k_inputs = tk.Frame(frame_left, bg=self.BG_CARD)
        frame_k_inputs.pack(fill="x", pady=2)
        tk.Label(frame_k_inputs, text="Số ngẫu nhiên k (0 < k < q) =", font=self.font_label, bg=self.BG_CARD).grid(
            row=0, column=0, sticky="e", padx=5)
        self.ent_k_enc = self.style_entry(frame_k_inputs, width=15)
        self.ent_k_enc.grid(row=0, column=1, pady=3)

        frame_k_btns = tk.Frame(frame_left, bg=self.BG_CARD)
        frame_k_btns.pack(pady=2)
        self.btn_random_k_enc = self.style_button(frame_k_btns, "Tạo k ngẫu nhiên", self.COLOR_BTN_DEF,
                                                  self.generate_k_enc_ui, width=15)
        self.btn_random_k_enc.grid(row=0, column=0, padx=5)
        self.btn_confirm_k_enc = self.style_button(frame_k_btns, "Xác nhận k & Tính K", self.COLOR_BTN_SEC,
                                                   self.confirm_k_enc, width=17)
        self.btn_confirm_k_enc.grid(row=0, column=1, padx=5)

        frame_K_res = tk.Frame(frame_left, bg=self.BG_CARD)
        frame_K_res.pack(fill="x", pady=3)
        tk.Label(frame_K_res, text="K = (YA^k mod q) =", font=self.font_bold, bg=self.BG_CARD, fg="#0D6EFD").grid(row=0,
                                                                                                                  column=0,
                                                                                                                  sticky="e",
                                                                                                                  padx=5)
        self.ent_K_enc = self.style_entry(frame_K_res, width=20)
        self.ent_K_enc.grid(row=0, column=1, pady=2)

        self.btn_encrypt = self.style_button(frame_left, "Thực hiện mã hóa", self.COLOR_BTN_PRI, self.action_encrypt,
                                             width=25)
        self.btn_encrypt.pack(pady=5)

        tk.Label(frame_left, text="Bản rõ được mã hóa gửi đi:", font=self.font_label, bg=self.BG_CARD).pack(anchor="w")
        self.txt_cipher_send = tk.Text(frame_left, height=3, font=self.font_label, relief="solid", bd=1)
        self.txt_cipher_send.pack(fill="x", pady=(2, 0))

        # Cột Phải: Giải mã
        frame_right = tk.LabelFrame(parent, text=" Giải mã ", font=self.font_title, bg=self.BG_CARD, padx=15, pady=5,
                                    relief="flat")
        frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        tk.Label(frame_right, text="Bản mã nhận được:", font=self.font_label, bg=self.BG_CARD).pack(anchor="w")
        self.txt_cipher_receive = tk.Text(frame_right, height=4, font=self.font_label, relief="solid", bd=1)
        self.txt_cipher_receive.pack(fill="x", pady=(2, 5))

        self.style_button(frame_right, "Thực hiện giải mã", self.COLOR_BTN_PRI, self.action_decrypt, width=25).pack(
            pady=10)

        tk.Label(frame_right, text="Bản được giải mã:", font=self.font_label, bg=self.BG_CARD).pack(anchor="w",
                                                                                                    pady=(5, 0))
        self.txt_plain_decrypted = tk.Text(frame_right, height=3, font=self.font_label, relief="solid", bd=1)
        self.txt_plain_decrypted.pack(fill="x", pady=(2, 10))

    # --- UI TAB 2: CHỮ KÝ SỐ ---
    def build_signature_ui(self, parent):
        frame_main = tk.LabelFrame(parent, text=" Thực hiện ký và Kiểm tra ", font=self.font_title, bg=self.BG_CARD,
                                   padx=20, pady=5, relief="flat")
        frame_main.pack(fill="both", expand=True, padx=10, pady=5)

        # Hàng 1: Quản lý k cho chữ ký số
        self.k_mode_sig = tk.IntVar(value=2)
        frame_k_mode = tk.Frame(frame_main, bg=self.BG_CARD)
        frame_k_mode.pack(fill="x", pady=2)
        tk.Radiobutton(frame_k_mode, text="Tùy chọn k", variable=self.k_mode_sig, value=1, command=self.toggle_k_sig,
                       font=self.font_label, bg=self.BG_CARD).pack(side="left")
        tk.Radiobutton(frame_k_mode, text="Tự động chọn k", variable=self.k_mode_sig, value=2,
                       command=self.toggle_k_sig, font=self.font_label, bg=self.BG_CARD).pack(side="left", padx=15)

        frame_k = tk.Frame(frame_main, bg=self.BG_CARD)
        frame_k.pack(fill="x", pady=2)
        tk.Label(frame_k, text="Số ngẫu nhiên k (0 < k < q-1 và gcd(k, q-1)=1):", font=self.font_label,
                 bg=self.BG_CARD).grid(row=0, column=0, padx=5, sticky="w")
        self.ent_k_sig = self.style_entry(frame_k, width=15)
        self.ent_k_sig.grid(row=0, column=1, padx=5)

        # CẬP NHẬT: Đổi tên nút thành "Tạo k ngẫu nhiên" và tăng width
        self.btn_random_k_sig = self.style_button(frame_k, "Tạo k ngẫu nhiên", self.COLOR_BTN_DEF,
                                                  self.generate_k_sig_ui, width=15)
        self.btn_random_k_sig.grid(row=0, column=2, padx=5)

        self.btn_confirm_k_sig = self.style_button(frame_k, "Xác nhận", self.COLOR_BTN_SEC, self.confirm_k_sig,
                                                   width=10)
        self.btn_confirm_k_sig.grid(row=0, column=3, padx=5)

        tk.Frame(frame_main, bg="#CED4DA", height=1).pack(fill="x", pady=8)  # Phân cách nhỏ

        # Hàng 2: Chọn File Ký
        frame_sign = tk.Frame(frame_main, bg=self.BG_CARD)
        frame_sign.pack(fill="x", pady=2)
        tk.Label(frame_sign, text="Chọn file thực hiện ký:", font=self.font_label, bg=self.BG_CARD).pack(anchor="w")

        frame_file_sign = tk.Frame(frame_sign, bg=self.BG_CARD)
        frame_file_sign.pack(fill="x", pady=2)
        self.ent_file_sign = self.style_entry(frame_file_sign, width=60)
        self.ent_file_sign.pack(side="left")
        tk.Button(frame_file_sign, text="...", font=self.font_bold, command=self.select_file_sign).pack(side="left",
                                                                                                        padx=5)
        self.btn_action_sign = self.style_button(frame_file_sign, "Thực hiện ký lên văn bản", self.COLOR_BTN_PRI,
                                                 self.action_sign, width=25)
        self.btn_action_sign.pack(side="left", padx=10)

        tk.Label(frame_sign, text="Tệp chữ ký được sinh ra (r, s):", font=self.font_label, bg=self.BG_CARD).pack(
            anchor="w", pady=(5, 0))
        self.txt_signature = tk.Text(frame_sign, height=2, font=self.font_label, relief="solid", bd=1)
        self.txt_signature.pack(fill="x", pady=2)

        tk.Frame(frame_main, bg="#CED4DA", height=1).pack(fill="x", pady=8)  # Phân cách nhỏ

        # Hàng 3: Chọn File Kiểm Tra
        frame_verify = tk.Frame(frame_main, bg=self.BG_CARD)
        frame_verify.pack(fill="x", pady=2)
        tk.Label(frame_verify, text="Chọn file cần kiểm tra:", font=self.font_label, bg=self.BG_CARD).pack(anchor="w")

        frame_file_veri = tk.Frame(frame_verify, bg=self.BG_CARD)
        frame_file_veri.pack(fill="x", pady=2)
        self.ent_file_verify = self.style_entry(frame_file_veri, width=60)
        self.ent_file_verify.pack(side="left")
        tk.Button(frame_file_veri, text="...", font=self.font_bold, command=self.select_file_verify).pack(side="left",
                                                                                                          padx=5)

        tk.Label(frame_verify, text="Nhập hoặc dán chuỗi chữ ký (r, s) vào đây:", font=self.font_label,
                 bg=self.BG_CARD).pack(anchor="w", pady=(5, 0))
        self.txt_signature_verify = tk.Text(frame_verify, height=2, font=self.font_label, relief="solid", bd=1)
        self.txt_signature_verify.pack(fill="x", pady=2)

        self.style_button(frame_verify, "Thực hiện Kiểm tra chữ ký", self.COLOR_BTN_PRI, self.action_verify,
                          width=25).pack(pady=5)

    # ==========================================
    # PHẦN 3: LOGIC TẠO KHÓA CHUNG
    # ==========================================
    def _set_entry(self, entry, text):
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, str(text))

    def _lock_entry(self, entry):
        entry.config(state="readonly")

    def _unlock_entry(self, entry):
        entry.config(state="normal")

    def toggle_key_mode(self):
        if self.key_mode.get() == 1:
            for ent in (self.ent_q, self.ent_a, self.ent_x):
                self._unlock_entry(ent)
                ent.delete(0, tk.END)
            self.lbl_ya_res.config(text="")
            self.lbl_pub_key.config(text="")
            self.lbl_priv_key.config(text="")
            self.btn_random_keys.config(state="disabled", bg="#CED4DA")
        else:
            self.btn_random_keys.config(state="normal", bg=self.COLOR_BTN_DEF)
            self.generate_random_keys_ui()
            for ent in (self.ent_q, self.ent_a, self.ent_x):
                self._lock_entry(ent)

    def generate_random_keys_ui(self):
        while True:
            q = random.randint(260, 5000)
            if core.is_prime(q): break
        while True:
            a = random.randint(2, q - 1)
            if core.is_primitive_root(a, q): break
        XA = random.randint(1, q - 2)

        self._set_entry(self.ent_q, q)
        self._set_entry(self.ent_a, a)
        self._set_entry(self.ent_x, XA)
        self.lbl_ya_res.config(text="")
        self.lbl_pub_key.config(text="")
        self.lbl_priv_key.config(text="")

    def confirm_keys(self):
        try:
            q = int(self.ent_q.get())
            a = int(self.ent_a.get())
            XA = int(self.ent_x.get())

            if not core.is_prime(q): raise ValueError("q phải là số nguyên tố!")
            if not core.is_primitive_root(a, q): raise ValueError(f"a phải là căn nguyên thủy của {q}!")
            if XA <= 0 or XA >= q - 1: raise ValueError(f"XA phải nằm trong khoảng (0, {q - 1})!")

            YA = core.generate_keys(q, a, XA)

            self.lbl_ya_res.config(text=f"{YA}")
            self.lbl_pub_key.config(text=f"{{{q}, {a}, {YA}}}")
            self.lbl_priv_key.config(text=f"{{{XA}}}")

            self.q, self.a, self.XA, self.YA = q, a, XA, YA

            for ent in (self.ent_q, self.ent_a, self.ent_x):
                self._lock_entry(ent)

            self.notebook.pack(fill="both", expand=True, padx=15, pady=(0, 10))

            self.toggle_k_enc()
            self.toggle_k_sig()

        except ValueError as e:
            messagebox.showerror("Lỗi nhập liệu", str(e))

    # ==========================================
    # PHẦN 4: LOGIC MÃ HÓA (TAB 1)
    # ==========================================
    def toggle_k_enc(self):
        self.k_enc_confirmed = None
        self._unlock_entry(self.ent_k_enc)
        self.ent_k_enc.delete(0, tk.END)
        self._set_entry(self.ent_K_enc, "")
        self._lock_entry(self.ent_K_enc)
        self.btn_encrypt.config(state="disabled", bg="#CED4DA")

        if self.k_mode_enc.get() == 1:
            self.btn_random_k_enc.config(state="disabled", bg="#CED4DA")
        else:
            self.btn_random_k_enc.config(state="normal", bg=self.COLOR_BTN_DEF)
            self.generate_k_enc_ui()

    def generate_k_enc_ui(self):
        if not self.q: return
        k = random.randint(1, self.q - 1)
        self._unlock_entry(self.ent_k_enc)
        self._set_entry(self.ent_k_enc, k)
        if self.k_mode_enc.get() == 2:
            self._lock_entry(self.ent_k_enc)
        self.k_enc_confirmed = None
        self._set_entry(self.ent_K_enc, "")
        self._lock_entry(self.ent_K_enc)
        self.btn_encrypt.config(state="disabled", bg="#CED4DA")

    def confirm_k_enc(self):
        k_str = self.ent_k_enc.get().strip()
        if not k_str.isdigit(): return messagebox.showerror("Lỗi", "k phải là một số nguyên!")
        k = int(k_str)
        # Điều kiện mã hóa k: 0 < k < q
        if k <= 0 or k >= self.q: return messagebox.showerror("Lỗi", f"k phải thuộc khoảng (0, {self.q})")

        self.k_enc_confirmed = k
        self._lock_entry(self.ent_k_enc)
        K_val = core.calc_exponent(self.YA, k, self.q)
        self._set_entry(self.ent_K_enc, K_val)
        self._lock_entry(self.ent_K_enc)
        self.btn_encrypt.config(state="normal", bg=self.COLOR_BTN_PRI)

    def action_encrypt(self):
        plain_text = self.txt_plain.get("1.0", tk.END).strip()
        if not plain_text: return messagebox.showwarning("Cảnh báo", "Vui lòng nhập bản rõ!")
        try:
            b64_encoded = core.encrypt_text(self.q, self.a, self.YA, plain_text, self.k_enc_confirmed)
            self.txt_cipher_send.delete("1.0", tk.END)
            self.txt_cipher_send.insert("1.0", b64_encoded)
            self.txt_cipher_receive.delete("1.0", tk.END)
            self.txt_cipher_receive.insert("1.0", b64_encoded)
        except ValueError as ve:
            messagebox.showerror("Lỗi Mã hóa", str(ve))

    def action_decrypt(self):
        b64_encoded = self.txt_cipher_receive.get("1.0", tk.END).strip()
        if not b64_encoded: return
        try:
            decrypted_text = core.decrypt_text(self.q, self.XA, b64_encoded)
            self.txt_plain_decrypted.delete("1.0", tk.END)
            self.txt_plain_decrypted.insert("1.0", decrypted_text)
        except Exception:
            messagebox.showerror("Lỗi", "Bản mã không hợp lệ hoặc đã bị can thiệp!")

    # ==========================================
    # PHẦN 5: LOGIC CHỮ KÝ SỐ (TAB 2)
    # ==========================================
    def toggle_k_sig(self):
        self.k_sig_confirmed = None
        self._unlock_entry(self.ent_k_sig)
        self.ent_k_sig.delete(0, tk.END)
        self.btn_action_sign.config(state="disabled", bg="#CED4DA")

        if hasattr(self, 'k_mode_sig'):
            if self.k_mode_sig.get() == 1:
                self.btn_random_k_sig.config(state="disabled", bg="#CED4DA")
            else:
                self.btn_random_k_sig.config(state="normal", bg=self.COLOR_BTN_DEF)
                self.generate_k_sig_ui()

    def generate_k_sig_ui(self):
        if not self.q: return
        # k chữ ký số: gcd(k, q-1) == 1
        while True:
            k = random.randint(1, self.q - 2)
            if math.gcd(k, self.q - 1) == 1:
                break
        self._unlock_entry(self.ent_k_sig)
        self._set_entry(self.ent_k_sig, k)

        if hasattr(self, 'k_mode_sig') and self.k_mode_sig.get() == 2:
            self._lock_entry(self.ent_k_sig)

        self.k_sig_confirmed = None
        self.btn_action_sign.config(state="disabled", bg="#CED4DA")

    def confirm_k_sig(self):
        k_str = self.ent_k_sig.get().strip()
        if not k_str.isdigit(): return messagebox.showerror("Lỗi", "k phải là một số nguyên!")
        k = int(k_str)

        # Điều kiện chữ ký số k: 0 < k < q-1
        if k <= 0 or k >= self.q - 1:
            return messagebox.showerror("Lỗi", f"k phải thuộc khoảng (0, {self.q - 1})")
        if math.gcd(k, self.q - 1) != 1:
            return messagebox.showerror("Lỗi Toán Học", f"k={k} không hợp lệ cho chữ ký số vì gcd(k, q-1) != 1")

        self.k_sig_confirmed = k
        self._lock_entry(self.ent_k_sig)
        self.btn_action_sign.config(state="normal", bg=self.COLOR_BTN_PRI)

    def select_file_sign(self):
        filepath = filedialog.askopenfilename(title="Chọn file để Ký")
        if filepath:
            self._set_entry(self.ent_file_sign, filepath)

    def select_file_verify(self):
        filepath = filedialog.askopenfilename(title="Chọn file để Kiểm tra")
        if filepath:
            self._set_entry(self.ent_file_verify, filepath)

    def action_sign(self):
        if not self.k_sig_confirmed:
            return messagebox.showwarning("Cảnh báo", "Vui lòng Xác nhận k trước!")

        filepath = self.ent_file_sign.get().strip()
        if not filepath:
            return messagebox.showwarning("Cảnh báo", "Vui lòng chọn file!")

        try:
            r, s = core.sign_file(self.q, self.a, self.XA, self.k_sig_confirmed, filepath)

            signature_str = json.dumps({"r": r, "s": s})

            self.txt_signature.delete("1.0", tk.END)
            self.txt_signature.insert("1.0", signature_str)

            self.txt_signature_verify.delete("1.0", tk.END)
            self.txt_signature_verify.insert("1.0", signature_str)
            self._set_entry(self.ent_file_verify, filepath)

            messagebox.showinfo("Thành công", "Đã tạo chữ ký số thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi Ký", f"Lỗi khi thực hiện ký: {str(e)}")

    def action_verify(self):
        filepath = self.ent_file_verify.get().strip()
        sig_str = self.txt_signature_verify.get("1.0", tk.END).strip()

        if not filepath or not sig_str:
            return messagebox.showwarning("Cảnh báo", "Vui lòng chọn file và dán chữ ký cần kiểm tra!")

        try:
            sig_dict = json.loads(sig_str)
            r = int(sig_dict["r"])
            s = int(sig_dict["s"])

            is_valid = core.verify_signature(self.q, self.a, self.YA, r, s, filepath)

            if is_valid:
                messagebox.showinfo("Kết quả Kiểm tra", "Chữ ký HỢP LỆ! Tệp không bị sửa đổi.")
            else:
                messagebox.showerror("Kết quả Kiểm tra", "Chữ ký KHÔNG HỢP LỆ! Cảnh báo tệp có thể đã bị chỉnh sửa.")
        except Exception as e:
            messagebox.showerror("Lỗi Định dạng", "Chuỗi chữ ký không đúng định dạng. Vui lòng kiểm tra lại.")