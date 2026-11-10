# Kế hoạch Bài kiểm tra 2

## Mục tiêu

Huấn luyện và so sánh mô hình phân loại ba nhãn ViHSD bằng baseline và các phương pháp tuyến tính. F1 Macro là chỉ số chính; Test chỉ dùng sau khi chọn cấu hình bằng Train/Validation. Tài liệu này triển khai phạm vi Tuần 6, chưa làm tìm kiếm tối ưu sâu của Tuần 8.

## Quy trình

| Bước | Thực hiện | Điều kiện nghiệm thu |
|---|---|---|
| A. Khởi tạo | Chốt rubric, nguồn tham khảo, phân công và hướng dẫn tự học | Tài liệu nói rõ việc của từng người; trạng thái cá nhân vẫn chờ xác nhận |
| B. Mô hình | Dummy majority; NB NumPy; NB scikit-learn; Logistic Regression; Linear SVC | NB NumPy xử lý sparse và xác suất/dự đoán khớp scikit-learn trên fixture |
| C. Pipeline/CV | Chuẩn hóa → PyVi/TF-IDF → classifier; 3-fold stratified và stratified-group | Vectorizer fit riêng trong từng fold; ghi số group giao giữa fold; không tuyên bố hết leakage nếu còn giao |
| D. Thực nghiệm | Development mặc định chỉ tải Train/Validation, chạy CV trên Train và chọn theo Validation. Final-test là lệnh riêng cần cấu hình đã khóa | Development không đọc nhãn Test hoặc ghi vào kết quả Test; kết quả mỗi mode/feature nằm ở thư mục mới; Test không ảnh hưởng lựa chọn |
| E. Phân tích | Metrics từng lớp, confusion matrix, chênh lệch Train–Validation, biểu đồ | Nhận xét dựa trên số thật; ghi hạn chế trùng nội dung và nhãn xung đột |
| F. Báo cáo/cá nhân | Báo cáo, Notebook, câu hỏi vấn đáp và thực hành | Mỗi sinh viên tự chạy, giải thích và lưu minh chứng; không suy ra từ commit Codex |

## Lệnh chính

Tạo môi trường và cài thư viện theo README. Sau khi đã có dữ liệu cục bộ đúng revision:

```powershell
python -m pytest -q tests
python scripts/run_exam2_experiments.py --mode development --features word --cv-folds 3
```

Lệnh và CLI mặc định ở chế độ `development`: chỉ dùng Train, CV và Validation. Mỗi lượt ghi vào thư mục mới dưới `reports/exam2_results/development/<feature>/<run-id>/`; các cấu hình word/combined có thư mục khác nhau. `--skip-group-cv` bỏ grouped CV và cần được ghi rõ khi báo cáo.

Chế độ `final-test` không dành cho bài thực hành. Chỉ gọi riêng sau khi đã khóa lựa chọn bằng Validation và truyền `--locked-config <selection.json>`; nó chỉ đánh giá cấu hình đó, không chọn lại. Kết quả được ghi vào `reports/exam2_results/final-test/<feature>/<model>/<run-id>/`, không ghi đè baseline cũ.

## Dữ liệu và quy tắc chống rò rỉ

- Giữ split chính thức và revision `88e81b36ca376867640dad9df295e0f7d499ab80`.
- Fit chuẩn hóa không học thống kê; fit TF-IDF trong từng fold trên phần train của fold.
- StratifiedKFold giúp phân bố lớp ổn định nhưng có thể để văn bản trùng đi qua fold.
- StratifiedGroupKFold gán cùng khóa văn bản chuẩn hóa vào một fold. Nêu số group xung đột và xác nhận số group giao bằng 0.
- Chọn mô hình theo Macro F1 Validation. Lệnh Development không nạp Test. Quy trình final-test riêng có thể được dùng sau khi khóa cấu hình; không dùng nhãn Test để chọn mô hình, tiền xử lý hoặc tạo mask.
- Không xóa/sửa dữ liệu gốc, nhãn hay split.

## Trạng thái cá nhân

Phân công là kế hoạch, chưa phải xác nhận hoàn thành. Tú và Tài cần tự chạy ít nhất một bài thực hành, ghi ngày/thao tác/kết quả/cách giải thích và tự xác nhận nội dung trước khi nộp.
