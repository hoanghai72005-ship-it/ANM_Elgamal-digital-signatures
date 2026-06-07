====================================================================
HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY CHƯƠNG TRÌNH HỆ MẬT MÃ ELGAMAL 
====================================================================

--------------------------------------------------------------------
1. YÊU CẦU HỆ THỐNG (CHUẨN BỊ)
--------------------------------------------------------------------
- Bước 1: Máy tính của bạn chỉ cần cài đặt Python (phiên bản 3.6 trở lên). 
  (Nếu chưa có, tải tại: https://www.python.org/downloads/ )
- Bước 2: Tải thư mục chứa mã nguồn này về máy. Đảm bảo trong thư mục 
  có đủ 3 file sau nằm cạnh nhau:
  1. main.py          (File gốc để chạy phần mềm)
  2. elgamal_gui.py   (Giao diện phần mềm) 
    - Cài đặt thư viện đồ họa: pip install sv-ttk
  3. elgamal_core.py  (Lõi thuật toán toán học)

--------------------------------------------------------------------
2. CÁCH KHỞI CHẠY PHẦN MỀM
--------------------------------------------------------------------
Cách đơn giản nhất:
- Mở thư mục chứa 3 file trên.
- Click đúp chuột (Double-click) vào file `main.py`.
- Run -> Giao diện phần mềm sẽ hiện lên!

--------------------------------------------------------------------
3. HƯỚNG DẪN SỬ DỤNG CƠ BẢN 
--------------------------------------------------------------------
Quy trình sử dụng phần mềm luôn bắt đầu từ việc TẠO KHÓA, sau đó bạn 
mới có thể sử dụng các chức năng ở Tab bên dưới.

📍 BƯỚC A: TẠO KHÓA CHUNG (Bắt buộc)
1. Ở khung "Giai đoạn sinh khóa" (phía trên cùng), bạn bấm nút 
   [Tạo khóa ngẫu nhiên]. Máy tính sẽ tự động bốc các số q, a, XA chuẩn 
   toán học cho bạn.
2. Bấm nút màu xanh [Tính YA & Xác nhận Khóa]. 
   => Khóa công khai và Khóa bí mật sẽ được chốt. Lúc này, 2 Tab tính năng 
   ở bên dưới sẽ hiện ra cho bạn sử dụng.

📍 BƯỚC B: MÃ HÓA & GIẢI MÃ CHUỖI TEXT (Tab 1)
1. Chọn Tab "Mã hóa Chuỗi Text".
2. Nhập một đoạn văn bản bất kỳ vào ô "Bản rõ".
3. Bấm [Tạo k ngẫu nhiên] -> Bấm [Xác nhận k & Tính K].
4. Bấm [Thực hiện mã hóa]. Bạn sẽ thấy bản rõ biến thành một chuỗi 
   ký tự Base64 loằng ngoằng.
5. Nhìn sang cột Giải mã bên phải, bấm [Thực hiện giải mã] để thấy 
   phần mềm khôi phục lại văn bản gốc của bạn!

📍 BƯỚC C: KÝ & KIỂM TRA CHỮ KÝ SỐ (Tab 2)
1. Chọn Tab "Chữ ký số ElGamal".
2. Khung Thực hiện ký: Bấm [Tạo k ngẫu nhiên] -> Bấm [Xác nhận].
3. Bấm nút [...] để chọn một File bất kỳ trên máy tính của bạn 
   (VD: 1 file ảnh, 1 file .docx, hoặc 1 file .txt).
4. Bấm [Thực hiện ký lên văn bản]. Một chuỗi Chữ ký (r, s) sẽ được sinh ra.
5. Khung Kiểm tra: Phần mềm đã tự động điền File và Chữ ký xuống khung 
   này cho bạn. Bấm [Thực hiện Kiểm tra chữ ký] -> Sẽ có thông báo 
   HỢP LỆ (vì file chưa bị sửa đổi).
   *Mẹo test:* Hãy thử mở file gốc ra, sửa 1 chữ, lưu lại, rồi bấm 
   kiểm tra lại, phần mềm sẽ báo KHÔNG HỢP LỆ ngay lập tức!

--------------------------------------------------------------------
4. MỘT SỐ LƯU Ý / TROUBLESHOOTING
--------------------------------------------------------------------
- Cảnh báo "Mã ký tự lớn hơn q": Khi mã hóa chữ cái, hệ thống dùng bảng 
  mã UTF-8 (từ 0 đến 255). Do đó, số nguyên tố `q` sinh ra phải lớn hơn 
  255. Nếu bạn tự nhập `q` quá nhỏ (ví dụ q=19 để test toán học) thì sẽ 
  không thể mã hóa chữ cái được.
- Đừng đổi tên 3 file Python: File `main.py` cần gọi `elgamal_gui.py` 
  và `elgamal_core.py`. Nếu bạn đổi tên file, chương trình sẽ báo lỗi 
  "ModuleNotFoundError".