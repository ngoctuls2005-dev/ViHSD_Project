# Bắt đầu tại đây – Hoàng Ngọc Tú

Tài liệu này là lộ trình để Tú tự làm và giải thích phần được giao. Việc dự án đã có số liệu không có nghĩa Tú đã tự thực hành. Trạng thái cá nhân hiện là **Chưa xác nhận hoàn thành**. Làm tại bản sao cục bộ; không huấn luyện mô hình và không đưa bình luận thật hoặc dữ liệu gốc lên GitHub.

## 1. Mở dự án bằng VS Code

1. Mở VS Code.
2. Chọn **File → Open Folder…** và chọn thư mục `ViHSD_Project` (thư mục có `README.md`, `src/`, `docs/` và `notebooks/`).
3. Mở Terminal → New Terminal. Kiểm tra thư mục hiện tại là gốc dự án bằng `Test-Path .\README.md`; kết quả cần là `True`.

**Kết quả mong đợi:** Explorer hiển thị các thư mục trên và terminal ở thư mục gốc dự án.

## 2. Chuẩn bị môi trường Python

Mở PowerShell trong thư mục gốc và chạy:

```powershell
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -r requirements-data.txt
```

Yêu cầu Python 3.10 trở lên. Nếu PowerShell chặn kích hoạt môi trường, không cần đổi chính sách máy: chọn interpreter `.venv\Scripts\python.exe` trong VS Code, hoặc chạy lệnh bằng `\.venv\Scripts\python.exe`.

Trong VS Code, bấm `Ctrl+Shift+P` → **Python: Select Interpreter** → chọn `.venv`. Cài/chọn hỗ trợ Python và Jupyter nếu VS Code đề nghị.

**Kết quả mong đợi:** lệnh `python --version` chạy được; các gói trong `requirements.txt` và `requirements-data.txt` đã sẵn sàng.

## 3. Mở Notebook và chọn dữ liệu thật

Mở [`notebooks/exam1_practice.ipynb`](../notebooks/exam1_practice.ipynb), chọn kernel `.venv` ở góc trên bên phải. Trước khi chạy, đảm bảo notebook không ở chế độ fixture:

```powershell
$env:VIHSD_NOTEBOOK_USE_FIXTURE = "0"
Test-Path .\data\raw\uitnlp_vihsd
```

Nếu kết quả `Test-Path` là `True`, notebook dùng bản ViHSD cục bộ. Nếu là `False`, đăng nhập bằng tài khoản Hugging Face đã được cấp quyền theo [hướng dẫn dữ liệu](data_access.md); notebook sẽ tải dữ liệu khi chạy code cell đầu tiên. Không dùng token/tài khoản của bạn khác và không gửi token qua chat.

Trong Notebook, chọn **Run All** hoặc chạy sáu code cell từ trên xuống. Các cell được nhận biết theo tiêu đề Markdown ngay phía trên:

1. Cell khởi tạo và nạp split: xác minh Train/Validation/Test, cột và kiểu dữ liệu.
2. **1. Phân bố nhãn**: đếm nhãn từng split và vẽ biểu đồ.
3. **2. Độ dài bình luận**: tạo bảng độ dài và biểu đồ.
4. **3. Chất lượng dữ liệu và trùng giữa split**: hiển thị số liệu; ví dụ văn bản trong bảng được thay bằng placeholder an toàn.
5. **4. Chuẩn hóa có kiểm soát**: tạo bản dẫn xuất và tóm tắt trước/sau.
6. **5. Chuẩn bị TF-IDF**: PyVi và ma trận thưa từ/ký tự; không huấn luyện bộ phân loại.

Notebook cần chạy từ đầu để các biến `frames`, `normalize_series` và `preprocessing_summary` có sẵn. Nếu cell lỗi, đọc lỗi, kiểm tra kernel `.venv`, rồi chạy lại cell bị lỗi sau khi sửa nguyên nhân; đừng chuyển sang fixture để ghi kết quả nghiên cứu.

**Kết quả mong đợi ở cell nạp:** Train 24.048 dòng, Validation 2.672, Test 6.680; tổng 33.400; cột `free_text` kiểu chuỗi và `label_id` kiểu số nguyên. Mã nhãn là 0=CLEAN, 1=OFFENSIVE, 2=HATE.

## 4. Tự đếm bình luận theo nhãn

Đọc bảng do code cell **1. Phân bố nhãn** in ra. Đối chiếu với số đã xác minh:

| Tập | CLEAN | OFFENSIVE | HATE |
|---|---:|---:|---:|
| Train | 19.886 | 1.606 | 2.556 |
| Validation | 2.190 | 212 | 270 |
| Test | 5.548 | 444 | 688 |

**Cách giải thích:** CLEAN là lớp đông nhất; OFFENSIVE là lớp ít nhất. Không suy ra chất lượng mô hình từ các số đếm này; ở Bài kiểm tra 1 chưa huấn luyện mô hình.

**Tự kiểm tra:** Tổng mỗi hàng có bằng kích thước split không? Vì sao cần nêu cả số lượng lẫn tỷ lệ?

## 5. Chạy và giải thích biểu đồ

Chạy code cell **1. Phân bố nhãn** và **2. Độ dài bình luận**. Xem biểu đồ đang hiển thị trong notebook. Kết quả được lưu cục bộ dưới `artifacts/practice/`, không cần đưa thư mục đó lên GitHub.

**Kết quả mong đợi:** phân bố nhãn cho thấy CLEAN chiếm đa số. Bảng độ dài thật có trung vị HATE là 59 ký tự, CLEAN và OFFENSIVE là 31. Số đếm khoảng trắng không đồng nghĩa số từ PyVi.

**Cách giải thích:** đây là mô tả dữ liệu, không phải quy tắc gán nhãn. Không kết luận câu dài chắc chắn là HATE. Nêu một nhận xét có số liệu và một giới hạn.

**Tự kiểm tra:** Biểu đồ nào đang mô tả tỷ lệ nhãn? Median khác mean như thế nào? Vì sao ngoại lệ có thể làm mean thay đổi?

## 6. Tính baseline F1 Macro lý thuyết

Mở phần 2 của [`reports/exam1_report.md`](../reports/exam1_report.md) và tự tính từ Train:

```text
Precision(CLEAN) = 19.886 / 24.048 = 0,8269
Recall(CLEAN) = 1
F1(CLEAN) = 2 × Precision × Recall / (Precision + Recall) = 0,9053
F1(OFFENSIVE) = F1(HATE) = 0
Macro F1 = (0,9053 + 0 + 0) / 3 = 0,3018 ≈ 0,302
```

**Giải thích:** Đây là phép tính lý thuyết cho cách luôn đoán CLEAN dựa trên phân bố lớp Train; không có mô hình được fit hay dự đoán. Nêu vì sao Accuracy 82,69% có thể gây ấn tượng sai khi hai lớp còn lại không được tìm thấy.

**Tự kiểm tra:** Nếu một lớp không bao giờ được dự đoán, F1 lớp đó là bao nhiêu? Vì sao Macro F1 cho mỗi lớp trọng số ngang nhau?

## 7. Giải thích phương án đánh giá bổ sung

Đọc tiểu mục **Phương án đánh giá bổ sung cho Bài kiểm tra 2** trong mục 6 của báo cáo. Nói lại bằng lời của mình:

1. Giữ nguyên Test chính thức.
2. Chọn mọi quy tắc và siêu tham số chỉ bằng Train/Validation, rồi khóa trước khi xem kết quả Test.
3. Báo cáo thêm phép nhạy cảm lọc theo văn bản: bỏ dòng Test có khóa văn bản chuẩn hóa xuất hiện trong Train.
4. Không dùng nhãn Test để chọn dòng, tiền xử lý hoặc mô hình; không xem kết quả để thay đổi lựa chọn.

**Kết quả mô tả đã xác minh:** phép lọc chỉ theo khóa văn bản còn 5.866 dòng Test, 5.776 chuỗi duy nhất. Đây là thiết kế cho bài sau, chưa phải kết quả mô hình.

**Tự kiểm tra:** Vì sao không thay Test chính thức bằng tập con? Điều gì có thể khiến kết quả trên tập con không đại diện cho toàn Test?

## 8. Tự làm phần thực hành của Tài

Ngoài Bài 1 và 3, Tú cần tự làm các Bài 2, 4 và 5 trong [`docs/practical_exercises.md`](practical_exercises.md): kiểm toán trùng, tìm nơi fit/transform của TF-IDF, và thử chuẩn hóa trên bản sao. Làm theo hướng dẫn trong mỗi bài, không chỉ đọc đáp án.

**Điều kiện đạt:** Tú có thể tự giải thích 792/797 chuỗi giao, 80 chuỗi xung đột, 96 cặp dòng khác nhãn; chỉ đúng `fit_transform` ở Train và `transform` ở Validation/Test; giải thích vì sao chuẩn hóa không sửa dữ liệu gốc.

## 9. Ôn vấn đáp

Mở [`docs/viva_questions.md`](viva_questions.md) và tự trả lời các câu 1–8 trước khi xem gợi ý. Trọng tâm: đầu vào/nhãn, mất cân bằng, F1 Macro, trùng chéo split, quy tắc chuẩn hóa, PyVi/TF-IDF và giới hạn của n-gram.

**Tự kiểm tra:** Có thể giải thích từng con số mà không đọc nguyên văn tài liệu không? Có phân biệt thống kê mô tả với kết luận mô hình không?

## 10. Ghi minh chứng đã tự thực hành

Sau khi thật sự hoàn thành, tự cập nhật mục **Hoàng Ngọc Tú** trong [`docs/contributions.md`](contributions.md): ngày, bài/tiêu chí, thao tác đã làm, kết quả tự giải thích, bằng chứng và xác nhận của Tú. Chỉ chia sẻ ảnh chụp không có bình luận thật, đường dẫn riêng tư hoặc thông tin tài khoản. Không đánh dấu thay cho Tài.

- [ ] Đã mở dự án và chọn đúng môi trường/kernel.
- [ ] Đã chạy Notebook từ đầu trên ViHSD thật.
- [ ] Đã tự làm bài chính 1 và 3.
- [ ] Đã tự làm phần học chéo 2, 4 và 5.
- [ ] Đã tự trả lời vấn đáp và cập nhật nhật ký của mình.
