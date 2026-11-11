# Tú – Bắt đầu Bài kiểm tra 2

## Bài thực hành 10–15 phút

Chỉ dùng Notebook ở chế độ fixture (`VIHSD_NOTEBOOK_USE_FIXTURE=1`) hoặc kết quả Development (Train/CV/Validation). Không mở nhãn Test và không dùng Test để chọn cấu hình.

1. Đọc trong `src/vihsd/models.py` phần `NumpyMultinomialNB.fit`: vai trò của `alpha`, prior lớp và vì sao vector TF-IDF phải không âm.
2. Mở `notebooks/exam2_practice.ipynb` và chạy notebook từ đầu. Notebook mặc định chỉ nạp Train và Validation; có thể bật fixture trong PowerShell:

   ```powershell
   $env:VIHSD_NOTEBOOK_USE_FIXTURE = "1"
   jupyter notebook notebooks/exam2_practice.ipynb
   ```

3. Trong cell tạo `estimators`, thêm `estimators["multinomial_nb_numpy"].set_params(alpha=0.5)` trước khi chạy cell so sánh mô hình. Ghi lại cấu hình và Validation Macro F1 theo lớp.
4. Giải thích baseline `DummyClassifier(most_frequent)`: luôn chọn lớp CLEAN trên dữ liệu hiện tại; Macro F1 phản ánh cả ba lớp. Không nhầm mức tham chiếu lý thuyết với kết quả classifier.
5. Đọc confusion matrix Validation của một mô hình: nêu true label, predicted label và số trường hợp. Không sao chép bình luận.

Thay đổi `alpha` chỉ là bài quan sát trên fixture hoặc Validation, không phải tìm kiếm tham số trên Test. Có thể khôi phục kernel sau bài tập; không commit thay đổi tạm thời trong mã dự án.

## Vì sao cần làm

Tiêu chí 1–2 yêu cầu giải thích thuật toán và baseline. Tiêu chí 6–7 yêu cầu đọc chỉ số theo lớp, confusion matrix và phân tích lỗi. Tiêu chí cá nhân 8–10 cần Tú tự trả lời và thao tác; tài liệu hay kiểm thử do Codex chuẩn bị không thay thế phần đó.

## Minh chứng cần ghi

Ghi ngày tự làm, fixture hay Development, lệnh/cell đã chạy, `alpha` trước/sau, chỉ số tổng hợp đã đọc và giải thích bằng lời của Tú. Không ghi nội dung bình luận, không đánh dấu hoàn thành nếu chưa tự làm và không gắn xác nhận giảng viên khi chưa có.

## Trạng thái thực hành của Tú (ngày 2026-11-11)

Các mục dưới đây ghi nhận theo phần Tú tự báo cáo ngày 2026-11-11. Codex đã tái lập các số liệu trên Train/Validation; việc ai trực tiếp thao tác và giải thích vẫn là tự xác nhận, chưa được quan sát độc lập. Phần vấn đáp chờ giảng viên đánh giá.

- [x] Đã đọc trong `src/vihsd/models.py` phần `NumpyMultinomialNB.fit`: hiểu rõ vai trò làm trơn của tham số Laplace `alpha`, prior lớp theo tần suất mẫu và yêu cầu ma trận TF-IDF không âm.
- [x] Đã chạy `notebooks/exam2_practice.ipynb` trên tập Development (Train 24.048, Validation 2.672 dòng).
- [x] Đã đổi `alpha` của `multinomial_nb_numpy` từ `1.0` thành `0.5`: ghi nhận Validation Macro F1 tăng từ 0,3029 lên 0,3127 (Train Macro F1 từ 0,3118 lên 0,4561; F1 HATE từ 0,0074 lên 0,0357).
- [x] Đã giải thích baseline `DummyClassifier(most_frequent)`: Macro F1 thực nghiệm trên Validation là 0,3003 (Accuracy 81,96% nhưng F1 OFFENSIVE=0 và F1 HATE=0); phân biệt rõ với mức lý thuyết 0,3018 tính trên Train ở Tuần 4.
- [x] Đã phân tích lỗi trong confusion matrix Validation: lỗi nghiêm trọng nhất là dự đoán nhầm lớp thiểu số thành lớp đa số (với NB alpha=0.5: HATE → CLEAN 265 ca, OFFENSIVE → CLEAN 208 ca; với Linear SVC balanced: HATE → CLEAN 89 ca, OFFENSIVE → CLEAN 109 ca).
- [x] Đã đọc và tự xác nhận khai báo AI ở mục 9 của báo cáo `reports/exam2_report.md`.
*(Chờ giảng viên quan sát và đánh giá trực tiếp qua buổi vấn đáp).*
