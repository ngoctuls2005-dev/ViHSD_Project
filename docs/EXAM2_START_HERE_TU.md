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
