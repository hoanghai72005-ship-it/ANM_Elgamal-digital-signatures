========================================================================
HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY CHƯƠNG TRÌNH HỆ MẬT MÃ ELGAMAL 
========================================================================

------------------------------------------------------------------------
1. CHUẨN BỊ MÔI TRƯỜNG
------------------------------------------------------------------------

a. Cài đặt Python: 
   Đảm bảo máy bạn đã cài sẵn Python (phiên bản 3.x). Có thể kiểm tra bằng 
   cách gõ lệnh `python --version` trong Terminal (hoặc Command Prompt).

b. Cài đặt C++ Build Tools (Rất quan trọng cho máy Windows):
   Vì code lõi viết bằng C++, Python cần một công cụ để biên dịch nó. 
   - Truy cập: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Tải về và mở file cài đặt (vs_BuildTools.exe).
   - Trong cửa sổ cài đặt, tìm và TÍCH CHỌN mục: "Desktop development with C++".
   - Bấm Install (Sẽ tốn vài GB tải xuống).
   - Cài xong, BẮT BUỘC KHỞI ĐỘNG LẠI phần mềm lập trình (VS Code, PyCharm, Terminal...).

------------------------------------------------------------------------
2. CÀI ĐẶT THƯ VIỆN VÀ BIÊN DỊCH CODE (BUILD)
------------------------------------------------------------------------

Mở Terminal (hoặc Command Prompt) và di chuyển (cd) vào thư mục chứa project này.

a. Cài đặt các thư viện cần thiết:
   Chạy lệnh sau để tải công cụ kết nối Python và C++:
   > pip install pybind11 setuptools wheel

b. Biên dịch lõi C++:
   Chạy lệnh sau để biến file "elgamal_core.cpp" thành thư viện Python:
   > python setup.py build_ext --inplace
   
   (Nếu lệnh chạy thành công, bạn sẽ thấy một file mới xuất hiện có đuôi 
   là .pyd (trên Windows) hoặc .so (trên Mac/Linux). Quá trình biên dịch 
   đã hoàn tất!)

------------------------------------------------------------------------
3. CHẠY CHƯƠNG TRÌNH
------------------------------------------------------------------------

- Sau khi đã có file .pyd, từ nay về sau bạn không cần chạy lại các bước trên nữa 
(trừ khi bạn chỉnh sửa code bên trong file C++).
- Click đúp chuột (Double-click) vào file `main.py`.
- Run -> Giao diện phần mềm sẽ hiện lên!

--------------------------------------------------------------------
4. HƯỚNG DẪN SỬ DỤNG CƠ BẢN 
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

========================================================================
CÁC LỖI THƯỜNG GẶP (TROUBLESHOOTING)
========================================================================

* Lỗi: "No module named 'setuptools'"
  -> Nguyên nhân: Bạn chưa cài công cụ build. 
  -> Cách sửa: Chạy lệnh `pip install setuptools` rồi build lại.

* Lỗi: "Microsoft Visual C++ 14.0 or greater is required"
  -> Nguyên nhân: Máy tính thiếu trình biên dịch C++.
  -> Cách sửa: Xem lại "PHẦN 1 - Bước 2" ở trên. Nhớ tích chọn đúng mục!

* Lỗi: Chữ "elgamal_core" bị gạch đỏ trong PyCharm
  -> Đây chỉ là do PyCharm không đọc được file nhị phân .pyd nên 
     nó báo lỗi giả. Code vẫn chạy bình thường, bạn cứ nhấn chạy file main.py nhé.