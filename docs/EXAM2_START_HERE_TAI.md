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
