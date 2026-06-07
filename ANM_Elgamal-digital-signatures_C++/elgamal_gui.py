import math
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
import sv_ttk

import elgamal_core as core


# LOP HIEN THI TOOLTIP (GHI CHU)
class GhiChu:
    def __init__(self, thanh_phan, van_ban, do_tre=400):
        self.thanh_phan = thanh_phan
        self.van_ban = van_ban
        self.do_tre = do_tre
        self.cua_so_ghi_chu = None
        self.id_len_lich = None
        self.thanh_phan.bind("<Enter>", self.len_lich_ghi_chu)
        self.thanh_phan.bind("<Leave>", self.an_ghi_chu)
        self.thanh_phan.bind("<ButtonPress>", self.an_ghi_chu)

    def len_lich_ghi_chu(self, event=None):
        self.id_len_lich = self.thanh_phan.after(self.do_tre, self.hien_thi_ghi_chu)

    def hien_thi_ghi_chu(self, event=None):
        if self.cua_so_ghi_chu: return
        x, y, _, _ = self.thanh_phan.bbox("insert")
        x += self.thanh_phan.winfo_rootx() + 25
        y += self.thanh_phan.winfo_rooty() + 20
        self.cua_so_ghi_chu = cua_so = tk.Toplevel(self.thanh_phan)
        cua_so.wm_overrideredirect(True)
        cua_so.wm_geometry(f"+{x}+{y}")
        nhan = ttk.Label(cua_so, text=self.van_ban, justify='left', relief='solid', borderwidth=1, padding=4)
        nhan.pack(ipadx=1)

    def an_ghi_chu(self, event=None):
        if self.id_len_lich:
            self.thanh_phan.after_cancel(self.id_len_lich)
            self.id_len_lich = None
        if self.cua_so_ghi_chu:
            self.cua_so_ghi_chu.destroy()
            self.cua_so_ghi_chu = None


# GIAO DIEN CHINH
class UngDungElGamal:
    def __init__(self, goc):
        self.goc = goc
        self.goc.title("Hệ mật mã ElGamal")

        self.goc.geometry("1100x750")
        self.goc.minsize(850, 620)

        try:
            self.goc.state('zoomed')
        except:
            pass

        self.q = self.a = self.XA = self.YA = None
        self.k_ma_hoa_da_chot = None
        self.k_chu_ky_da_chot = None

        self.che_do_khoa = tk.IntVar(value=2)
        self.che_do_k_ma_hoa = tk.IntVar(value=2)
        self.che_do_k_chu_ky = tk.IntVar(value=2)

        self.font_title = ("Segoe UI", 11, "bold")
        self.font_label = ("Segoe UI", 10)
        self.font_bold = ("Segoe UI", 10, "bold")

        sv_ttk.set_theme("light")

        self.tao_khung_sinh_khoa()
        self.tao_cac_the()
        self.chuyen_doi_che_do_khoa()

        self.chuyen_doi_k_ma_hoa()
        self.chuyen_doi_k_chu_ky()

        self.cap_nhat_mau_chu()

    def cap_nhat_mau_chu(self):
        mau_nen = "#ffffff"
        mau_chu = "#000000"
        mau_con_tro = "#000000"

        danh_sach_o_chu = [
            self.o_chu_ban_ro, self.o_chu_ban_ma_gui, self.o_chu_ban_ma_nhan,
            self.o_chu_ban_giai_ma, self.o_chu_chu_ky, self.o_chu_chu_ky_xac_thuc
        ]
        for o_chu in danh_sach_o_chu:
            o_chu.configure(bg=mau_nen, fg=mau_chu, insertbackground=mau_con_tro)

    def tao_o_chu_co_cuon(self, cha, chieu_cao):
        khung = ttk.Frame(cha)
        thanh_phan_chu = tk.Text(khung, height=chieu_cao, font=("Segoe UI", 10), wrap="word", bd=1, relief="solid")
        thanh_cuon = ttk.Scrollbar(khung, orient="vertical", command=thanh_phan_chu.yview)
        thanh_phan_chu.configure(yscrollcommand=thanh_cuon.set)

        thanh_phan_chu.pack(side="left", fill="both", expand=True)
        thanh_cuon.pack(side="right", fill="y")
        return khung, thanh_phan_chu

    def hanh_dong_sao_chep(self, thanh_phan_chu):
        noi_dung = thanh_phan_chu.get("1.0", tk.END).strip()
        if noi_dung:
            self.goc.clipboard_clear()
            self.goc.clipboard_append(noi_dung)
            messagebox.showinfo("Clipboard", "📋 Đã sao chép nội dung thành công!")
        else:
            messagebox.showwarning("Cảnh báo", "Không có nội dung để sao chép!")

    def hanh_dong_luu_tep(self, thanh_phan_chu, ten_mac_dinh):
        noi_dung = thanh_phan_chu.get("1.0", tk.END).strip()
        if not noi_dung: return messagebox.showwarning("Cảnh báo", "Không có nội dung để lưu!")

        loai_tep = [("Text Document", "*.txt"), ("JSON File", "*.json"), ("All Files", "*.*")]
        duong_dan = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=loai_tep, initialfile=ten_mac_dinh,
                                                 title="Lưu file về máy")
        if duong_dan:
            try:
                if duong_dan.endswith('.json'):
                    with open(duong_dan, 'w', encoding='utf-8') as f:
                        json.dump({"data": noi_dung}, f, indent=4)
                else:
                    with open(duong_dan, 'w', encoding='utf-8') as f:
                        f.write(noi_dung)
                messagebox.showinfo("Thành công", f"💾 Đã lưu tệp thành công tại:\n{duong_dan}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")

    def hanh_dong_luu_chu_ky(self):
        noi_dung = self.o_chu_chu_ky.get("1.0", tk.END).strip()
        if not noi_dung: return messagebox.showwarning("Cảnh báo", "Không có chữ ký để lưu!")

        loai_tep = [("JSON File", "*.json"), ("Text Document", "*.txt"), ("All Files", "*.*")]
        duong_dan = filedialog.asksaveasfilename(defaultextension=".json", filetypes=loai_tep,
                                                 initialfile="chu_ky_so.json", title="Lưu chữ ký về máy")

        if duong_dan:
            try:
                if duong_dan.endswith('.json'):
                    try:
                        tu_dien_chu_ky = json.loads(noi_dung)
                        if hasattr(self, 'r_vua_ky') and tu_dien_chu_ky.get(
                                "r") == self.r_vua_ky and tu_dien_chu_ky.get("s") == self.s_vua_ky:
                            tu_dien_chu_ky["m"] = getattr(self, 'm_vua_ky', None)
                        with open(duong_dan, 'w', encoding='utf-8') as f:
                            json.dump(tu_dien_chu_ky, f, indent=4)
                    except:
                        with open(duong_dan, 'w', encoding='utf-8') as f:
                            json.dump({"data": noi_dung}, f, indent=4)
                else:
                    with open(duong_dan, 'w', encoding='utf-8') as f:
                        f.write(noi_dung)
                messagebox.showinfo("Thành công", f"💾 Đã lưu chữ ký thành công tại:\n{duong_dan}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu chữ ký: {str(e)}")

    def _dat_o_nhap(self, o_nhap, van_ban):
        o_nhap.config(state="normal")
        o_nhap.delete(0, tk.END)
        o_nhap.insert(0, str(van_ban))

    def _khoa_o_nhap(self, o_nhap):
        o_nhap.config(state="readonly")

    def _mo_khoa_o_nhap(self, o_nhap):
        o_nhap.config(state="normal")

    # PHAN 1: KHUNG TAO KHOA CHUNG
    def tao_khung_sinh_khoa(self):
        self.khung_khoa = ttk.LabelFrame(self.goc, text=" 🔑 Giai đoạn sinh khóa ", padding=10)
        self.khung_khoa.pack(fill="x", padx=15, pady=10)

        self.khung_khoa.columnconfigure(0, weight=1)
        self.khung_khoa.columnconfigure(1, weight=1)

        khung_vao = ttk.Frame(self.khung_khoa)
        khung_vao.grid(row=0, column=0, sticky="nw", padx=10)

        khung_radio = ttk.Frame(khung_vao)
        khung_radio.pack(anchor="w", pady=(0, 5))
        ttk.Radiobutton(khung_radio, text="Tùy chọn (Nhập tay)", variable=self.che_do_khoa, value=1,
                        command=self.chuyen_doi_che_do_khoa).pack(side="left", padx=(0, 20))
        ttk.Radiobutton(khung_radio, text="Tự động chọn", variable=self.che_do_khoa, value=2,
                        command=self.chuyen_doi_che_do_khoa).pack(side="left")

        luoi_vao = ttk.Frame(khung_vao)
        luoi_vao.pack(fill="x")

        ttk.Label(luoi_vao, text="Chọn số nguyên tố q đủ lớn:").grid(row=0, column=0, sticky="w", pady=2)
        self.o_nhap_q = ttk.Entry(luoi_vao, width=25)
        self.o_nhap_q.grid(row=0, column=1, padx=10)
        GhiChu(self.o_nhap_q,
               "Yêu cầu: q phải là một số nguyên tố đủ lớn.\n(Khuyến nghị q > 255 để mã hóa an toàn bảng mã UTF-8).")

        ttk.Label(luoi_vao, text="Chọn a là căn nguyên thủy của q (a < q):").grid(row=1, column=0, sticky="w", pady=2)
        self.o_nhap_a = ttk.Entry(luoi_vao, width=25)
        self.o_nhap_a.grid(row=1, column=1, padx=10)
        GhiChu(self.o_nhap_a, "Yêu cầu: a phải là một căn nguyên thủy của q và a < q.")

        ttk.Label(luoi_vao, text="Chọn Khóa bí mật XA (XA < q - 1):").grid(row=2, column=0, sticky="w", pady=2)
        self.o_nhap_x = ttk.Entry(luoi_vao, width=25)
        self.o_nhap_x.grid(row=2, column=1, padx=10)
        GhiChu(self.o_nhap_x, "Yêu cầu: Khóa bí mật XA phải thỏa mãn XA < q - 1.")

        khung_ra = ttk.Frame(self.khung_khoa)
        khung_ra.grid(row=0, column=1, sticky="ne", padx=10)

        khung_nut_khoa = ttk.Frame(khung_ra)
        khung_nut_khoa.pack(anchor="w", pady=(0, 5))
        self.nut_khoa_ngau_nhien = ttk.Button(khung_nut_khoa, text="🎲 Tạo khóa ngẫu nhiên",
                                              command=self.tao_khoa_ngau_nhien_ui)
        self.nut_khoa_ngau_nhien.pack(side="left", padx=(0, 10))
        self.nut_xac_nhan_khoa = ttk.Button(khung_nut_khoa, text="✔️ Tính YA & Xác nhận Khóa", style="Accent.TButton",
                                            command=self.xac_nhan_khoa)
        self.nut_xac_nhan_khoa.pack(side="left")

        luoi_ra = ttk.Frame(khung_ra)
        luoi_ra.pack(fill="x", pady=5)
        ttk.Label(luoi_ra, text="Tính toán: YA = a^XA mod q =").grid(row=0, column=0, sticky="w", pady=2)
        self.nhan_ket_qua_ya = ttk.Label(luoi_ra, text="", font=("", 10, "bold"))
        self.nhan_ket_qua_ya.grid(row=0, column=1, sticky="w", padx=10)

        ttk.Label(luoi_ra, text="Khóa công khai {q, a, YA}:").grid(row=1, column=0, sticky="w", pady=2)
        self.nhan_khoa_cong_khai = ttk.Label(luoi_ra, text="", font=("", 10, "bold"), foreground="#D9534F")
        self.nhan_khoa_cong_khai.grid(row=1, column=1, sticky="w", padx=10)

        ttk.Label(luoi_ra, text="Khóa bí mật {XA}:").grid(row=2, column=0, sticky="w", pady=2)
        self.nhan_khoa_bi_mat = ttk.Label(luoi_ra, text="", font=("", 10, "bold"), foreground="#D9534F")
        self.nhan_khoa_bi_mat.grid(row=2, column=1, sticky="w", padx=10)

    # PHAN 2: THIET KE CAC TABS
    def tao_cac_the(self):
        self.so_tay = ttk.Notebook(self.goc)

        self.the_ma_hoa = ttk.Frame(self.so_tay)
        self.so_tay.add(self.the_ma_hoa, text=" 🔏 Mã hóa Chuỗi Text ")
        self.tao_giao_dien_ma_hoa(self.the_ma_hoa)

        self.the_chu_ky = ttk.Frame(self.so_tay)
        self.so_tay.add(self.the_chu_ky, text=" ✍️ Chữ ký số ElGamal ")
        self.tao_giao_dien_chu_ky(self.the_chu_ky)

        self.so_tay.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # --- UI TAB 1: MA HOA VAN BAN ---
    def tao_giao_dien_ma_hoa(self, cha):
        cha.columnconfigure(0, weight=4)
        cha.columnconfigure(1, weight=5)
        cha.rowconfigure(0, weight=1)

        khung_trai = ttk.LabelFrame(cha, text=" Thực hiện Mã hóa ", padding=10)
        khung_trai.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(khung_trai, text="Bản rõ:").pack(anchor="w")
        khung_ban_ro, self.o_chu_ban_ro = self.tao_o_chu_co_cuon(khung_trai, 2)
        khung_ban_ro.pack(fill="both", expand=True, pady=(2, 5))

        khung_giua = ttk.Frame(khung_trai)
        khung_giua.pack(fill="x", pady=5)
        khung_giua.columnconfigure(1, weight=1)

        khung_dieu_khien_k = ttk.Frame(khung_giua)
        khung_dieu_khien_k.grid(row=0, column=0, sticky="w", pady=2)
        ttk.Radiobutton(khung_dieu_khien_k, text="Tùy chọn k", variable=self.che_do_k_ma_hoa, value=1,
                        command=self.chuyen_doi_k_ma_hoa).pack(side="left")
        ttk.Radiobutton(khung_dieu_khien_k, text="Tự động", variable=self.che_do_k_ma_hoa, value=2,
                        command=self.chuyen_doi_k_ma_hoa).pack(side="left", padx=10)

        ttk.Label(khung_dieu_khien_k, text="Số ngẫu nhiên k =").pack(side="left", padx=(5, 2))
        self.o_nhap_k_ma_hoa = ttk.Entry(khung_dieu_khien_k, width=10)
        self.o_nhap_k_ma_hoa.pack(side="left", padx=2)
        GhiChu(self.o_nhap_k_ma_hoa,
               "k là số ngẫu nhiên chỉ dùng một lần (Session key).\nĐiều kiện bắt buộc: 0 < k < q")

        self.nut_k_ma_hoa_ngau_nhien = ttk.Button(khung_dieu_khien_k, text="🎲 Tạo k ngẫu nhiên",
                                                  command=self.tao_k_ma_hoa_ngau_nhien_ui)
        self.nut_k_ma_hoa_ngau_nhien.pack(side="left", padx=5)

        self.nut_xac_nhan_k_ma_hoa = ttk.Button(khung_giua, text="✔️ Xác nhận k", style="Accent.TButton",
                                                command=self.xac_nhan_k_ma_hoa, width=18)
        self.nut_xac_nhan_k_ma_hoa.grid(row=0, column=2, sticky="e", pady=2)

        khung_ket_qua_K = ttk.Frame(khung_giua)
        khung_ket_qua_K.grid(row=1, column=0, sticky="w", pady=2)
        ttk.Label(khung_ket_qua_K, text="K = (YA^k mod q) =", font=("", 10, "bold")).pack(side="left")
        self.o_nhap_K_lon_ma_hoa = ttk.Entry(khung_ket_qua_K, width=15)
        self.o_nhap_K_lon_ma_hoa.pack(side="left", padx=5)

        self.nut_ma_hoa = ttk.Button(khung_giua, text="🔒 Thực hiện mã hóa", style="Accent.TButton",
                                     command=self.hanh_dong_ma_hoa, width=18)
        self.nut_ma_hoa.grid(row=1, column=2, sticky="e", pady=2)

        ttk.Label(khung_trai, text="Bản rõ được mã hóa gửi đi:").pack(anchor="w")
        khung_ban_ma_gui, self.o_chu_ban_ma_gui = self.tao_o_chu_co_cuon(khung_trai, 3)
        khung_ban_ma_gui.pack(fill="both", expand=True, pady=(2, 2))

        khung_cong_cu_ma_hoa = ttk.Frame(khung_trai)
        khung_cong_cu_ma_hoa.pack(anchor="e")
        ttk.Button(khung_cong_cu_ma_hoa, text="📋 Copy",
                   command=lambda: self.hanh_dong_sao_chep(self.o_chu_ban_ma_gui)).pack(side="left", padx=2)
        ttk.Button(khung_cong_cu_ma_hoa, text="💾 Lưu File",
                   command=lambda: self.hanh_dong_luu_tep(self.o_chu_ban_ma_gui, "ban_ma")).pack(side="left")

        # Cột Phải: Giai ma
        khung_phai = ttk.LabelFrame(cha, text=" Thực hiện Giải mã ", padding=10)
        khung_phai.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        ttk.Label(khung_phai, text="Bản mã nhận được:").pack(anchor="w")
        khung_ban_ma_nhan, self.o_chu_ban_ma_nhan = self.tao_o_chu_co_cuon(khung_phai, 4)
        khung_ban_ma_nhan.pack(fill="both", expand=True, pady=(2, 5))

        self.nut_giai_ma = ttk.Button(khung_phai, text="🔓 Thực hiện giải mã", style="Accent.TButton",
                                      command=self.hanh_dong_giai_ma)
        self.nut_giai_ma.pack(pady=5)

        ttk.Label(khung_phai, text="Bản được giải mã:").pack(anchor="w")
        khung_ban_giai_ma, self.o_chu_ban_giai_ma = self.tao_o_chu_co_cuon(khung_phai, 3)
        khung_ban_giai_ma.pack(fill="both", expand=True, pady=(2, 5))

        khung_cong_cu_giai_ma = ttk.Frame(khung_phai)
        khung_cong_cu_giai_ma.pack(anchor="e")
        ttk.Button(khung_cong_cu_giai_ma, text="📋 Copy",
                   command=lambda: self.hanh_dong_sao_chep(self.o_chu_ban_giai_ma)).pack(side="left", padx=2)
        ttk.Button(khung_cong_cu_giai_ma, text="💾 Lưu File",
                   command=lambda: self.hanh_dong_luu_tep(self.o_chu_ban_giai_ma, "ban_giai_ma")).pack(side="left")

    # --- UI TAB 2: CHU KY SO TREN TEP TIN ---
    def tao_giao_dien_chu_ky(self, cha):
        cha.columnconfigure(0, weight=1)
        cha.rowconfigure(0, weight=1)
        cha.rowconfigure(1, weight=1)

        khung_ky = ttk.LabelFrame(cha, text=" ✍️ Thực hiện Ký ", padding=10)
        khung_ky.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        khung_k_chu_ky = ttk.Frame(khung_ky)
        khung_k_chu_ky.pack(fill="x", pady=5)
        khung_k_chu_ky.columnconfigure(1, weight=1)

        khung_radio_sig = ttk.Frame(khung_k_chu_ky)
        khung_radio_sig.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 5))
        ttk.Radiobutton(khung_radio_sig, text="Tùy chọn k", variable=self.che_do_k_chu_ky, value=1,
                        command=self.chuyen_doi_k_chu_ky).pack(side="left")
        ttk.Radiobutton(khung_radio_sig, text="Tự động chọn k", variable=self.che_do_k_chu_ky, value=2,
                        command=self.chuyen_doi_k_chu_ky).pack(side="left", padx=10)

        ttk.Label(khung_k_chu_ky, text="Số ngẫu nhiên k =").grid(row=1, column=0, sticky="w", padx=(0, 5), pady=3)

        self.o_nhap_k_chu_ky = ttk.Entry(khung_k_chu_ky)
        self.o_nhap_k_chu_ky.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=3)
        GhiChu(self.o_nhap_k_chu_ky,
               "Điều kiện bắt buộc cho chữ ký số:\n- 0 < k < q-1\n- gcd(k, q-1) = 1 (k và q-1 phải nguyên tố cùng nhau)")

        self.nut_k_chu_ky_ngau_nhien = ttk.Button(khung_k_chu_ky, text="🎲 Tạo k ngẫu nhiên",
                                                  command=self.tao_k_chu_ky_ngau_nhien_ui)
        self.nut_k_chu_ky_ngau_nhien.grid(row=1, column=2, sticky="e", padx=(10, 15), pady=3)

        self.nut_xac_nhan_k_chu_ky = ttk.Button(khung_k_chu_ky, text="✔️ Xác nhận k", style="Accent.TButton",
                                                command=self.xac_nhan_k_chu_ky)
        self.nut_xac_nhan_k_chu_ky.grid(row=1, column=3, sticky="ew", pady=3)

        khung_tep_ky = ttk.Frame(khung_ky)
        khung_tep_ky.pack(fill="x", pady=5)
        ttk.Label(khung_tep_ky, text="Chọn file thực hiện ký:").pack(side="left")
        self.o_nhap_tep_ky = ttk.Entry(khung_tep_ky)
        self.o_nhap_tep_ky.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(khung_tep_ky, text="📁", width=3, command=self.chon_tep_de_ky).pack(side="left")
        self.nut_thuc_hien_ky = ttk.Button(khung_tep_ky, text="✍️ Thực hiện ký lên văn bản", style="Accent.TButton",
                                           command=self.hanh_dong_ky)
        self.nut_thuc_hien_ky.pack(side="right", padx=(10, 0))

        ttk.Label(khung_ky, text="Tệp chữ ký được sinh ra (r, s):").pack(anchor="w", pady=(5, 0))
        khung_hien_thi_chu_ky, self.o_chu_chu_ky = self.tao_o_chu_co_cuon(khung_ky, 2)
        khung_hien_thi_chu_ky.pack(fill="both", expand=True, pady=2)

        khung_cong_cu_chu_ky = ttk.Frame(khung_ky)
        khung_cong_cu_chu_ky.pack(anchor="e")
        ttk.Button(khung_cong_cu_chu_ky, text="📋 Copy",
                   command=lambda: self.hanh_dong_sao_chep(self.o_chu_chu_ky)).pack(side="left", padx=2)
        ttk.Button(khung_cong_cu_chu_ky, text="💾 Lưu Chữ Ký", command=self.hanh_dong_luu_chu_ky).pack(side="left")

        # Nửa dưới: XAC THUC CHU KY
        khung_xac_thuc = ttk.LabelFrame(cha, text=" 🛡️ Kiểm tra (Xác thực) ", padding=10)
        khung_xac_thuc.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        khung_tep_xac_thuc = ttk.Frame(khung_xac_thuc)
        khung_tep_xac_thuc.pack(fill="x", pady=5)
        ttk.Label(khung_tep_xac_thuc, text="Chọn file cần kiểm tra (Bản nhận được):").pack(side="left")
        self.o_nhap_tep_xac_thuc = ttk.Entry(khung_tep_xac_thuc)
        self.o_nhap_tep_xac_thuc.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(khung_tep_xac_thuc, text="📁", width=3, command=self.chon_tep_de_xac_thuc).pack(side="left")

        khung_tieu_de_chu_ky = ttk.Frame(khung_xac_thuc)
        khung_tieu_de_chu_ky.pack(fill="x", pady=(5, 0))
        ttk.Label(khung_tieu_de_chu_ky, text="Nhập hoặc tải lên chuỗi chữ ký (r, s) tương ứng vào đây:").pack(
            side="left")
        ttk.Button(khung_tieu_de_chu_ky, text="📁 Tải file chữ ký", command=self.chon_tep_chu_ky_de_xac_thuc).pack(
            side="right")

        khung_hien_thi_xac_thuc, self.o_chu_chu_ky_xac_thuc = self.tao_o_chu_co_cuon(khung_xac_thuc, 2)
        khung_hien_thi_xac_thuc.pack(fill="both", expand=True, pady=2)

        self.nut_thuc_hien_xac_thuc = ttk.Button(khung_xac_thuc, text="🛡️ Thực hiện Kiểm tra chữ ký",
                                                 style="Accent.TButton", command=self.hanh_dong_xac_thuc)
        self.nut_thuc_hien_xac_thuc.pack(pady=5)

    def chuyen_doi_che_do_khoa(self):
        if self.che_do_khoa.get() == 1:
            for o_nhap in (self.o_nhap_q, self.o_nhap_a, self.o_nhap_x):
                self._mo_khoa_o_nhap(o_nhap)
                o_nhap.delete(0, tk.END)
            self.nhan_ket_qua_ya.config(text="")
            self.nhan_khoa_cong_khai.config(text="")
            self.nhan_khoa_bi_mat.config(text="")
            self.nut_khoa_ngau_nhien.state(["disabled"])
        else:
            self.nut_khoa_ngau_nhien.state(["!disabled"])
            self.tao_khoa_ngau_nhien_ui()
            for o_nhap in (self.o_nhap_q, self.o_nhap_a, self.o_nhap_x):
                self._khoa_o_nhap(o_nhap)

    def tao_khoa_ngau_nhien_ui(self):
        while True:
            q = random.randint(260, 5000)
            if core.kiem_tra_so_nguyen_to(q): break
        while True:
            a = random.randint(2, q - 1)
            if core.kiem_tra_can_nguyen_thuy(a, q): break
        XA = random.randint(1, q - 2)

        self._dat_o_nhap(self.o_nhap_q, q)
        self._dat_o_nhap(self.o_nhap_a, a)
        self._dat_o_nhap(self.o_nhap_x, XA)
        self.nhan_ket_qua_ya.config(text="")
        self.nhan_khoa_cong_khai.config(text="")
        self.nhan_khoa_bi_mat.config(text="")

    def xac_nhan_khoa(self):
        try:
            q = int(self.o_nhap_q.get())
            a = int(self.o_nhap_a.get())
            XA = int(self.o_nhap_x.get())

            if not core.kiem_tra_so_nguyen_to(q): raise ValueError("q phải là số nguyên tố!")
            if not core.kiem_tra_can_nguyen_thuy(a, q): raise ValueError(f"a phải là căn nguyên thủy của {q}!")
            if XA <= 0 or XA >= q - 1: raise ValueError(f"XA phải nằm trong khoảng (0, {q - 1})!")

            YA = core.tao_khoa(q, a, XA)

            self.nhan_ket_qua_ya.config(text=f"{YA}")
            self.nhan_khoa_cong_khai.config(text=f"{{{q}, {a}, {YA}}}")
            self.nhan_khoa_bi_mat.config(text=f"{{{XA}}}")

            self.q, self.a, self.XA, self.YA = q, a, XA, YA

            for o_nhap in (self.o_nhap_q, self.o_nhap_a, self.o_nhap_x):
                self._khoa_o_nhap(o_nhap)

            self.chuyen_doi_k_ma_hoa()
            self.chuyen_doi_k_chu_ky()

        except ValueError as e:
            messagebox.showerror("Lỗi nhập liệu", str(e))

    def _phan_hoi_loi_bat_dong_bo(self, tieu_de, thong_diep, danh_sach_nut):
        self.goc.config(cursor="")
        messagebox.showerror(tieu_de, thong_diep)
        for nut in danh_sach_nut:
            nut.state(["!disabled"])

    def chuyen_doi_k_ma_hoa(self):
        self.k_ma_hoa_da_chot = None
        self._mo_khoa_o_nhap(self.o_nhap_k_ma_hoa)
        self.o_nhap_k_ma_hoa.delete(0, tk.END)
        self._dat_o_nhap(self.o_nhap_K_lon_ma_hoa, "")
        self._khoa_o_nhap(self.o_nhap_K_lon_ma_hoa)
        self.nut_ma_hoa.state(["disabled"])

        if self.che_do_k_ma_hoa.get() == 1:
            self.nut_k_ma_hoa_ngau_nhien.state(["disabled"])
        else:
            self.nut_k_ma_hoa_ngau_nhien.state(["!disabled"])
            self.tao_k_ma_hoa_ngau_nhien_ui()

    def tao_k_ma_hoa_ngau_nhien_ui(self):
        if not self.q: return
        k = random.randint(1, self.q - 1)
        self._mo_khoa_o_nhap(self.o_nhap_k_ma_hoa)
        self._dat_o_nhap(self.o_nhap_k_ma_hoa, k)
        if self.che_do_k_ma_hoa.get() == 2:
            self._khoa_o_nhap(self.o_nhap_k_ma_hoa)
        self.k_ma_hoa_da_chot = None
        self._dat_o_nhap(self.o_nhap_K_lon_ma_hoa, "")
        self._khoa_o_nhap(self.o_nhap_K_lon_ma_hoa)
        self.nut_ma_hoa.state(["disabled"])

    def xac_nhan_k_ma_hoa(self):
        if not self.q: return messagebox.showwarning("Cảnh báo", "Vui lòng Tính YA & Xác nhận Khóa chung trước!")
        chuoi_k = self.o_nhap_k_ma_hoa.get().strip()
        if not chuoi_k.isdigit(): return messagebox.showerror("Lỗi", "k phải là một số nguyên!")
        k = int(chuoi_k)
        if k <= 0 or k >= self.q: return messagebox.showerror("Lỗi", f"k phải thuộc khoảng (0, {self.q})")

        self.k_ma_hoa_da_chot = k
        self._khoa_o_nhap(self.o_nhap_k_ma_hoa)
        Gia_tri_K = core.tinh_luy_thua(self.YA, k, self.q)
        self._dat_o_nhap(self.o_nhap_K_lon_ma_hoa, Gia_tri_K)
        self._khoa_o_nhap(self.o_nhap_K_lon_ma_hoa)
        self.nut_ma_hoa.state(["!disabled"])

    def hanh_dong_ma_hoa(self):
        ban_ro = self.o_chu_ban_ro.get("1.0", tk.END).strip()
        if not ban_ro: return messagebox.showwarning("Cảnh báo", "Vui lòng nhập bản rõ!")

        self.nut_ma_hoa.state(["disabled"])
        self.goc.config(cursor="watch")

        def luong_xu_ly():
            try:
                chuoi_b64 = core.ma_hoa_van_ban(self.q, self.a, self.YA, ban_ro, self.k_ma_hoa_da_chot)
                self.goc.after(0, self._phan_hoi_giao_dien_ma_hoa, chuoi_b64)
            except ValueError as ve:
                self.goc.after(0, self._phan_hoi_loi_bat_dong_bo, "Lỗi Mã hóa", str(ve), [self.nut_ma_hoa])
            except Exception as e:
                self.goc.after(0, self._phan_hoi_loi_bat_dong_bo, "Lỗi Hệ thống", str(e), [self.nut_ma_hoa])

        threading.Thread(target=luong_xu_ly, daemon=True).start()

    def _phan_hoi_giao_dien_ma_hoa(self, chuoi_b64):
        self.o_chu_ban_ma_gui.delete("1.0", tk.END)
        self.o_chu_ban_ma_gui.insert("1.0", chuoi_b64)
        self.o_chu_ban_ma_nhan.delete("1.0", tk.END)
        self.o_chu_ban_ma_nhan.insert("1.0", chuoi_b64)
        self.nut_ma_hoa.state(["!disabled"])
        self.goc.config(cursor="")

    def hanh_dong_giai_ma(self):
        chuoi_b64 = self.o_chu_ban_ma_nhan.get("1.0", tk.END).strip()
        if not chuoi_b64: return

        self.nut_giai_ma.state(["disabled"])
        self.goc.config(cursor="watch")

        def luong_xu_ly():
            try:
                chuoi_giai_ma = core.giai_ma_van_ban(self.q, self.XA, chuoi_b64)
                self.goc.after(0, self._phan_hoi_giao_dien_giai_ma, chuoi_giai_ma)
            except Exception:
                self.goc.after(0, self._phan_hoi_loi_bat_dong_bo, "Lỗi", "Bản mã không hợp lệ hoặc đã bị can thiệp!",
                               [self.nut_giai_ma])

        threading.Thread(target=luong_xu_ly, daemon=True).start()

    def _phan_hoi_giao_dien_giai_ma(self, chuoi_giai_ma):
        self.o_chu_ban_giai_ma.delete("1.0", tk.END)
        self.o_chu_ban_giai_ma.insert("1.0", chuoi_giai_ma)
        self.nut_giai_ma.state(["!disabled"])
        self.goc.config(cursor="")

    def chuyen_doi_k_chu_ky(self):
        self.k_chu_ky_da_chot = None
        self._mo_khoa_o_nhap(self.o_nhap_k_chu_ky)
        self.o_nhap_k_chu_ky.delete(0, tk.END)
        self.nut_thuc_hien_ky.state(["disabled"])

        if hasattr(self, 'che_do_k_chu_ky'):
            if self.che_do_k_chu_ky.get() == 1:
                self.nut_k_chu_ky_ngau_nhien.state(["disabled"])
            else:
                self.nut_k_chu_ky_ngau_nhien.state(["!disabled"])
                self.tao_k_chu_ky_ngau_nhien_ui()

    def tao_k_chu_ky_ngau_nhien_ui(self):
        if not self.q: return
        while True:
            k = random.randint(1, self.q - 2)
            if math.gcd(k, self.q - 1) == 1:
                break
        self._mo_khoa_o_nhap(self.o_nhap_k_chu_ky)
        self._dat_o_nhap(self.o_nhap_k_chu_ky, k)

        if hasattr(self, 'che_do_k_chu_ky') and self.che_do_k_chu_ky.get() == 2:
            self._khoa_o_nhap(self.o_nhap_k_chu_ky)

        self.k_chu_ky_da_chot = None
        self.nut_thuc_hien_ky.state(["disabled"])

    def xac_nhan_k_chu_ky(self):
        if not self.q: return messagebox.showwarning("Cảnh báo", "Vui lòng Tính YA & Xác nhận Khóa chung trước!")
        chuoi_k = self.o_nhap_k_chu_ky.get().strip()
        if not chuoi_k.isdigit(): return messagebox.showerror("Lỗi", "k phải là một số nguyên!")
        k = int(chuoi_k)
        if k <= 0 or k >= self.q - 1: return messagebox.showerror("Lỗi", f"k phải thuộc khoảng (0, {self.q - 1})")
        if math.gcd(k, self.q - 1) != 1:
            return messagebox.showerror("Lỗi Toán Học", f"k={k} không hợp lệ cho chữ ký số vì gcd(k, q-1) != 1")

        self.k_chu_ky_da_chot = k
        self._khoa_o_nhap(self.o_nhap_k_chu_ky)
        self.nut_thuc_hien_ky.state(["!disabled"])

    def chon_tep_de_ky(self):
        duong_dan_tep = filedialog.askopenfilename(title="Chọn file để Ký")
        if duong_dan_tep:
            self._dat_o_nhap(self.o_nhap_tep_ky, duong_dan_tep)

    def chon_tep_de_xac_thuc(self):
        duong_dan_tep = filedialog.askopenfilename(title="Chọn file để Kiểm tra")
        if duong_dan_tep:
            self._dat_o_nhap(self.o_nhap_tep_xac_thuc, duong_dan_tep)

    def chon_tep_chu_ky_de_xac_thuc(self):
        duong_dan_tep = filedialog.askopenfilename(title="Chọn file Chữ ký",
                                                   filetypes=[("JSON/TXT Files", "*.json *.txt"), ("All Files", "*.*")])
        if duong_dan_tep:
            try:
                with open(duong_dan_tep, 'r', encoding='utf-8') as f:
                    noi_dung = f.read()
                    try:
                        du_lieu = json.loads(noi_dung)
                        if "data" in du_lieu and isinstance(du_lieu["data"], str):
                            du_lieu_trong = json.loads(du_lieu["data"])
                            r = du_lieu_trong.get("r")
                            s = du_lieu_trong.get("s")
                            m_goc = du_lieu_trong.get("m")
                        else:
                            r = du_lieu.get("r")
                            s = du_lieu.get("s")
                            m_goc = du_lieu.get("m")

                        if r is not None and s is not None:
                            self.m_da_tai_xac_thuc = m_goc
                            self.r_da_tai_xac_thuc = r
                            self.s_da_tai_xac_thuc = s

                            chuoi_hien_thi = json.dumps({"r": r, "s": s})
                            self.o_chu_chu_ky_xac_thuc.delete("1.0", tk.END)
                            self.o_chu_chu_ky_xac_thuc.insert("1.0", chuoi_hien_thi)
                        else:
                            self.o_chu_chu_ky_xac_thuc.delete("1.0", tk.END)
                            self.o_chu_chu_ky_xac_thuc.insert("1.0", noi_dung)
                    except json.JSONDecodeError:
                        self.o_chu_chu_ky_xac_thuc.delete("1.0", tk.END)
                        self.o_chu_chu_ky_xac_thuc.insert("1.0", noi_dung)
            except Exception as e:
                messagebox.showerror("Lỗi Đọc File", f"Không thể đọc file chữ ký: {str(e)}")

    def hanh_dong_ky(self):
        if not self.k_chu_ky_da_chot: return messagebox.showwarning("Cảnh báo", "Vui lòng Xác nhận k trước!")
        duong_dan_tep = self.o_nhap_tep_ky.get().strip()
        if not duong_dan_tep: return messagebox.showwarning("Cảnh báo", "Vui lòng chọn file!")

        self.nut_thuc_hien_ky.state(["disabled"])
        self.goc.config(cursor="watch")

        def luong_xu_ly():
            try:
                r, s, m_goc = core.ky_tep_tin(self.q, self.a, self.XA, self.k_chu_ky_da_chot, duong_dan_tep)

                self.r_vua_ky = r
                self.s_vua_ky = s
                self.m_vua_ky = m_goc

                chuoi_chu_ky = json.dumps({"r": r, "s": s})
                self.goc.after(0, self._phan_hoi_giao_dien_ky, chuoi_chu_ky)
            except Exception as e:
                self.goc.after(0, self._phan_hoi_loi_bat_dong_bo, "Lỗi Ký", f"Lỗi khi thực hiện ký: {str(e)}",
                               [self.nut_thuc_hien_ky])

        threading.Thread(target=luong_xu_ly, daemon=True).start()

    def _phan_hoi_giao_dien_ky(self, chuoi_chu_ky):
        self.o_chu_chu_ky.delete("1.0", tk.END)
        self.o_chu_chu_ky.insert("1.0", chuoi_chu_ky)
        self.nut_thuc_hien_ky.state(["!disabled"])
        self.goc.config(cursor="")
        self.m_da_tai_xac_thuc = None
        messagebox.showinfo("Thành công", "Đã tạo chữ ký số thành công!")

    def hanh_dong_xac_thuc(self):
        duong_dan_tep = self.o_nhap_tep_xac_thuc.get().strip()
        chuoi_chu_ky = self.o_chu_chu_ky_xac_thuc.get("1.0", tk.END).strip()

        if not duong_dan_tep or not chuoi_chu_ky:
            return messagebox.showwarning("Cảnh báo", "Vui lòng chọn file và nhập/tải lên chữ ký cần kiểm tra!")

        self.nut_thuc_hien_xac_thuc.state(["disabled"])
        self.goc.config(cursor="watch")

        def luong_xu_ly():
            try:
                try:
                    tu_dien_chu_ky = json.loads(chuoi_chu_ky)
                    r = int(tu_dien_chu_ky["r"])
                    s = int(tu_dien_chu_ky["s"])
                except (json.JSONDecodeError, KeyError, ValueError):
                    self.goc.after(0, self._phan_hoi_loi_bat_dong_bo, "Lỗi Chữ ký",
                                   "❌ CẤU TRÚC CHỮ KÝ BỊ PHÁ HOẠI!\nChuỗi chữ ký không đúng định dạng hoặc chứa ký tự lạ.",
                                   [self.nut_thuc_hien_xac_thuc])
                    return

                if not (0 < r < self.q) or not (0 <= s < self.q - 1):
                    self.goc.after(0, self._phan_hoi_loi_bat_dong_bo, "Lỗi Chữ ký",
                                   "❌ CHỮ KÝ BỊ LÀM GIẢ!\nCác thông số (r, s) nằm ngoài giới hạn cho phép của hệ thống khóa hiện tại.",
                                   [self.nut_thuc_hien_xac_thuc])
                    return

                m_goc = None
                if hasattr(self, "m_da_tai_xac_thuc") and getattr(self, "m_da_tai_xac_thuc", None) is not None:
                    m_goc = self.m_da_tai_xac_thuc
                elif hasattr(self, "m_vua_ky") and getattr(self, "m_vua_ky", None) is not None:
                    m_goc = self.m_vua_ky

                if m_goc is not None:
                    trang_thai = core.xac_minh_chu_ky_chi_tiet(self.q, self.a, self.YA, r, s, int(m_goc), duong_dan_tep)
                    self.goc.after(0, self._phan_hoi_xac_thuc_chi_tiet_ui, trang_thai)
                else:
                    hop_le = core.xac_minh_chu_ky(self.q, self.a, self.YA, r, s, duong_dan_tep)
                    trang_thai = "HOP_LE" if hop_le else "SAI_DINH_DANG"
                    self.goc.after(0, self._phan_hoi_xac_thuc_chi_tiet_ui, trang_thai)

            except Exception as e:
                self.goc.after(0, self._phan_hoi_loi_bat_dong_bo, "Lỗi Hệ thống", f"Có lỗi bất ngờ xảy ra: {str(e)}",
                               [self.nut_thuc_hien_xac_thuc])

        threading.Thread(target=luong_xu_ly, daemon=True).start()

    def _phan_hoi_xac_thuc_chi_tiet_ui(self, trang_thai):
        self.nut_thuc_hien_xac_thuc.state(["!disabled"])
        self.goc.config(cursor="")

        if trang_thai == "HOP_LE":
            messagebox.showinfo("Kết quả", "✅ CHỮ KÝ HỢP LỆ!\nVăn bản toàn vẹn và chữ ký chính xác")
        elif trang_thai == "TEP_BI_SUA_DOI":
            messagebox.showerror("Kết quả: Không hợp lệ",
                                 "❌ VĂN BẢN KHÔNG TOÀN VẸN!\n\nVăn bản đã bị sửa đổi so với lúc ký (Mã băm không khớp)")
        elif trang_thai == "CHU_KY_BI_SUA_DOI":
            messagebox.showerror("Kết quả: Không hợp lệ",
                                 "❌ CHỮ KÝ BỊ SỬA ĐỔI!\n\nVăn bản không bị thay đổi, nhưng thông số chữ ký (r, s) đã bị làm giả hoặc chỉnh sửa")
        elif trang_thai == "CA_HAI_BI_SUA_DOI":
            messagebox.showerror("Kết quả: Không hợp lệ",
                                 "❌ VĂN BẢN VÀ CHỮ KÝ ĐỀU BỊ SỬA ĐỔI!\n\nVăn bản không toàn vẹn và bản thân chữ ký cũng không khớp")
        else:
            messagebox.showerror("Kết quả: Không hợp lệ",
                                 "❌ KIỂM TRA THẤT BẠI!\n\nChữ ký không khớp với văn bản (Chữ ký được nhập thủ công từ nguồn ngoài nên hệ thống không lưu vết mã băm để phân loại lỗi chi tiết)")