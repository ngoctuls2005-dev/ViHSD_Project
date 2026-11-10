# Kế hoạch Bài kiểm tra 2

## Mục tiêu

Huấn luyện và so sánh mô hình phân loại ba nhãn ViHSD bằng baseline và các phương pháp tuyến tính. F1 Macro là chỉ số chính; Test chỉ dùng sau khi chọn cấu hình bằng Train/Validation. Tài liệu này triển khai phạm vi Tuần 6, chưa làm tìm kiếm tối ưu sâu của Tuần 8.

## Quy trình

| Bước | Thực hiện | Điều kiện nghiệm thu |
|---|---|---|
| A. Khởi tạo | Chốt rubric, nguồn tham khảo, phân công và hướng dẫn tự học | Tài liệu nói rõ việc của từng người; trạng thái cá nhân vẫn chờ xác nhận |
| B. Mô hình | Dummy majority; NB NumPy; NB scikit-learn; Logistic Regression; Linear SVC | NB NumPy xử lý sparse và xác suất/dự đoán khớp scikit-learn trên fixture |
| C. Pipeline/CV | Chuẩn hóa → PyVi/TF-IDF → classifier; 3-fold stratified và stratified-group | Vectorizer fit riêng trong từng fold; ghi số group giao giữa fold; không tuyên bố hết leakage nếu còn giao |
| D. Thực nghiệm | CV trên Train; so sánh Validation; khóa mô hình theo Macro F1 Validation; Test chính thức và phép nhạy cảm không giao văn bản Train | Test không ảnh hưởng lựa chọn; lưu chỉ số tổng hợp, không lưu text/dự đoán theo dòng |
| E. Phân tích | Metrics từng lớp, confusion matrix, chênh lệch Train–Validation, biểu đồ | Nhận xét dựa trên số thật; ghi hạn chế trùng nội dung và nhãn xung đột |
| F. Báo cáo/cá nhân | Báo cáo, Notebook, câu hỏi vấn đáp và thực hành | Mỗi sinh viên tự chạy, giải thích và lưu minh chứng; không suy ra từ commit Codex |

## Lệnh chính

Tạo môi trường và cài thư viện theo README. Sau khi đã có dữ liệu cục bộ đúng revision:

```powershell
python -m pytest -q tests
python scripts/run_exam2_experiments.py --features word --cv-folds 3
```

Lượt khởi đầu dùng word TF-IDF để giảm thời gian. Có thể chạy `--features combined` sau khi pipeline cơ bản ổn định; lựa chọn cuối phải được chốt bằng Validation. `--skip-group-cv` chỉ dùng khi cần chạy thử nhanh và phải ghi rõ việc bỏ qua.

## Dữ liệu và quy tắc chống rò rỉ

- Giữ split chính thức và revision `88e81b36ca376867640dad9df295e0f7d499ab80`.
- Fit chuẩn hóa không học thống kê; fit TF-IDF trong từng fold trên phần train của fold.
- StratifiedKFold giúp phân bố lớp ổn định nhưng có thể để văn bản trùng đi qua fold.
- StratifiedGroupKFold gán cùng khóa văn bản chuẩn hóa vào một fold. Nêu số group xung đột và xác nhận số group giao bằng 0.
- Chọn mô hình theo macro F1 Validation. Sau khi khóa lựa chọn, dùng Test chính thức một lần và báo thêm phép nhạy cảm đã định nghĩa bằng văn bản Train/Test, không dùng nhãn Test để tạo mask.
- Không xóa/sửa dữ liệu gốc, nhãn hay split.

## Trạng thái cá nhân

Phân công là kế hoạch, chưa phải xác nhận hoàn thành. Tú và Tài cần tự chạy ít nhất một bài thực hành, ghi ngày/thao tác/kết quả/cách giải thích và tự xác nhận nội dung trước khi nộp.
