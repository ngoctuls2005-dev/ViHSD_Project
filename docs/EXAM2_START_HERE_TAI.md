# Tài – Bắt đầu Bài kiểm tra 2

## Bài thực hành 10–15 phút

Chỉ dùng Notebook ở chế độ fixture (`VIHSD_NOTEBOOK_USE_FIXTURE=1`) hoặc kết quả Development (Train/CV/Validation). Không mở nhãn Test và không dùng Test để chọn cấu hình.

1. Lần theo `src/vihsd/experiment.py` và `src/vihsd/model_evaluation.py`: mỗi fold tạo vectorizer mới, fit trên phần Train của fold và chỉ transform phần giữ lại.
2. Mở `notebooks/exam2_practice.ipynb` và chạy từ đầu. Có thể chạy fixture trên PowerShell:

   ```powershell
   $env:VIHSD_NOTEBOOK_USE_FIXTURE = "1"
   jupyter notebook notebooks/exam2_practice.ipynb
   ```

3. Trước cell CV và Validation, đổi `C` của Logistic Regression hoặc Linear SVC, ví dụ `estimators["logistic_regression_balanced"].set_params(C=0.5)`. Chạy lại cell CV và bảng Validation, không đổi nhiều tham số cùng lúc.
4. So sánh mean/std Macro F1 giữa các fold. Nêu mean là hiệu quả trung bình theo fold; std mô tả độ biến động giữa các fold, không phải độ bất định trên toàn bộ quần thể.
5. Giải thích vì sao `StratifiedGroupKFold` giữ các văn bản trùng trong một fold và giới hạn của cách này với văn bản gần giống hoặc nhóm có nhãn xung đột.

Nếu muốn chạy CLI trên dữ liệu thật, lệnh mặc định cũng chỉ dùng Development:

```powershell
python scripts/run_exam2_experiments.py --mode development --features word --cv-folds 3
```

Mỗi lượt có thư mục kết quả riêng. Không chạy `--mode final-test` cho bài thực hành.

## Vì sao cần làm

Tiêu chí 3–5 yêu cầu Pipeline không rò rỉ, chương trình chạy được và CV đúng. Dữ liệu có văn bản trùng nên cần giải thích hai cách chia. Tiêu chí cá nhân 8–10 yêu cầu Tài tự giải thích và thao tác; mã do Codex tạo không xác nhận thay phần đó.

## Minh chứng cần ghi

Ghi ngày tự làm, fixture hay Development, lệnh/cell, cấu hình `C` hoặc `class_weight`, file kết quả Validation/CV và cách diễn giải mean/std bằng lời của Tài. Không ghi nội dung bình luận, không đánh dấu hoàn thành nếu chưa tự làm và không gắn xác nhận giảng viên khi chưa có.

## Trạng thái thực hành của Tài (ngày 2026-11-11)

Các mục dưới đây ghi nhận theo phần Tài tự báo cáo ngày 2026-11-11. Codex đã tái lập các số liệu trên Train/Validation; việc ai trực tiếp thao tác và giải thích vẫn là tự xác nhận, chưa được quan sát độc lập. Phần vấn đáp chờ giảng viên đánh giá.

- [x] Đã lần theo `src/vihsd/experiment.py` và `src/vihsd/model_evaluation.py`: kiểm chứng Pipeline và CV fit TF-IDF riêng từng fold trên phần Train của fold đó, ngăn ngừa rò rỉ dữ liệu.
- [x] Đã giải thích nguyên lý và giới hạn của `StratifiedGroupKFold`: gom toàn bộ các chuỗi văn bản trùng lặp vào cùng một fold để tránh đánh giá quá lạc quan; nhận thức rõ giới hạn là chỉ gom được trùng chuỗi tuyệt đối sau chuẩn hóa, không gom được văn bản tương đồng ngữ nghĩa và 132 nhóm có nhãn xung đột.
- [x] Đã chạy thử nghiệm đổi `C` từ `1.0` thành `0.5` cho `linear_svc_balanced` và `logistic_regression_balanced`: ghi lại kết quả 3-fold CV (Stratified và Grouped) cùng Validation Macro F1.
- [x] Đã giải thích ý nghĩa CV mean và std: mean đo hiệu năng trung bình giữa các fold; std thể hiện độ phân tán/biến động giữa các lát cắt fold.
- [x] Đã giải thích lý do không chọn mô hình/siêu tham số theo Test (tránh rò rỉ / snooping; bảo toàn tính khách quan của tập Test chính thức).
- [x] Đã đọc và tự xác nhận khai báo AI ở mục 9 của báo cáo `reports/exam2_report.md`.
*(Chờ giảng viên quan sát và đánh giá trực tiếp qua buổi vấn đáp).*
