# ViHSD: Phát hiện ngôn từ thù ghét và xúc phạm

Dự án môn Học máy nghiên cứu phân loại bình luận mạng xã hội tiếng Việt thành `CLEAN`, `OFFENSIVE` và `HATE` bằng bộ dữ liệu ViHSD của UIT.

## HƯỚNG DẪN DÀNH CHO THÀNH VIÊN NHÓM

- [Hoàng Ngọc Tú – Bắt đầu tại đây](docs/START_HERE_TU.md)
- [Lê Quang Tài – Bắt đầu tại đây](docs/START_HERE_TAI.md)
- [Bảng phân công chung](docs/TEAM_ASSIGNMENTS.md)
- [Năm bài thực hành](docs/practical_exercises.md)
- [Nhật ký đóng góp cá nhân](docs/contributions.md)
- [Báo cáo Bài kiểm tra 1](reports/exam1_report.md)
- [Kế hoạch Bài kiểm tra 2](docs/exam2_plan.md)
- [Tài liệu nghiên cứu Bài kiểm tra 2](docs/exam2_research.md)
- [Phân công Bài kiểm tra 2](docs/EXAM2_TEAM_ASSIGNMENTS.md)
- [Hướng dẫn riêng cho Tú](docs/EXAM2_START_HERE_TU.md)
- [Hướng dẫn riêng cho Tài](docs/EXAM2_START_HERE_TAI.md)
- [Câu hỏi vấn đáp và thực hành Bài kiểm tra 2](docs/exam2_viva_questions.md)
- [Báo cáo Bài kiểm tra 2](reports/exam2_report.md)

## Trạng thái

Sản phẩm Bài kiểm tra 1 được dùng làm nền cho Bài kiểm tra 2 – tuần 6. Lượt baseline thật đã chạy trên nhánh `codex/exam2-week6`: 3-fold CV, so sánh Validation, khóa Linear SVC balanced theo Validation Macro F1 `0,6184`, sau đó Test Macro F1 `0,6017`. Kết quả grouped CV thấp hơn stratified CV, phù hợp rủi ro văn bản trùng đã ghi nhận. Đây chưa phải tối ưu cuối; chưa xác nhận sinh viên hoàn tất phần cá nhân hoặc vấn đáp. Xem [báo cáo Tuần 6](reports/exam2_report.md) và [nhật ký](docs/PROGRESS.md).

Mức tham chiếu Macro F1 của chiến lược luôn dự đoán CLEAN là `0,302`, tính từ phân bố nhãn Train; đây là phép tính lý thuyết, không phải kết quả mô hình. Kiểm toán phát hiện 80 chuỗi giao Train–Test có xung đột nhãn; quy trình đánh giá bổ sung và giới hạn này được ghi trong báo cáo.

Nguồn chính thức là [`uitnlp/vihsd` trên Hugging Face](https://huggingface.co/datasets/uitnlp/vihsd). Cần đăng nhập và chấp thuận điều kiện truy cập. Hugging Face ghi metadata MIT; README tác giả nói dữ liệu chỉ dùng cho nghiên cứu. Vì phạm vi hai ghi chú chưa được làm rõ, dữ liệu và bình luận gốc không được đưa lên GitHub.

## Cài đặt và tải/phân tích dữ liệu thật

Yêu cầu Python 3.10 trở lên. Trên Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m pip install -r requirements-data.txt
```

Nếu chưa xác thực Hugging Face, chạy `hf auth login` và nhập token trực tiếp tại lời nhắc cục bộ; không gửi token qua hội thoại hoặc lưu token trong dự án. Sau đó chạy:

```powershell
python scripts/run_real_dataset_analysis.py
```

Lệnh tải `uitnlp/vihsd` nếu chưa có bản cục bộ, lưu split gốc vào `data/raw/uitnlp_vihsd/`, tạo các bảng tổng hợp cục bộ trong `artifacts/real_vihsd/`, và sinh hai biểu đồ an toàn trong `reports/figures/`. Hai thư mục dữ liệu/đầu ra cục bộ bị Git bỏ qua. Xem [hướng dẫn tải và điều kiện truy cập](docs/data_access.md).

Notebook [`notebooks/exam1_practice.ipynb`](notebooks/exam1_practice.ipynb) mặc định đọc dữ liệu thật ở `data/raw/uitnlp_vihsd/` (hoặc tải nếu chưa có). Notebook chỉ hiển thị thống kê tổng hợp, không in bình luận. Chế độ fixture kỹ thuật có thể bật bằng biến `VIHSD_NOTEBOOK_USE_FIXTURE=1`; kết quả fixture không phải kết quả nghiên cứu.

## Kiểm thử

Chạy unit test:

```powershell
python -m unittest discover -s tests -v
```

Kiểm thử tích hợp dữ liệu thật được bật riêng, cần phiên Hugging Face có quyền:

```powershell
$env:VIHSD_RUN_INTEGRATION = "1"
python -m unittest discover -s tests -v
```

Notebook và kiểm thử của Bài kiểm tra 1 không huấn luyện bộ phân loại. Baseline Tuần 6 được mô tả riêng ở mục dưới. Không công khai `data/raw/`, các bảng chứa từ/cụm từ trích từ bình luận, hay notebook có output bình luận thật.

## Chạy thực nghiệm Bài kiểm tra 2

Sau khi tải dữ liệu thật và xác minh phiên bản, chạy ba fold trên Train, so sánh trên Validation, khóa mô hình theo Macro F1 Validation rồi mới đánh giá Test:

```powershell
python scripts/run_exam2_experiments.py --features word --cv-folds 3
```

Script mặc định chạy cả StratifiedKFold và StratifiedGroupKFold theo khóa văn bản chuẩn hóa. Để rút ngắn lượt thử ban đầu, có thể thêm `--skip-group-cv`; phải ghi rõ khi báo cáo. `--features combined` bật word và character TF-IDF. Kết quả chỉ chứa metrics, ma trận nhầm lẫn, biểu đồ và metadata tổng hợp trong `reports/exam2_results/`; không ghi bình luận hay dự đoán từng dòng. Chỉ chấm Test sau khi khóa lựa chọn theo Validation; không dùng kết quả Test để đổi pipeline hoặc mô hình.

Các mô hình: Dummy majority, MultinomialNB NumPy, MultinomialNB scikit-learn, Logistic Regression và Linear SVM. Đây là cấu hình khởi đầu, không phải kết luận mô hình cuối cho Bài kiểm tra 2.

## Tài liệu dự án

- [Nguồn, quyền truy cập và tái tạo dữ liệu](docs/data_access.md)
- [Giải thích phương pháp đánh giá](docs/evaluation_guide.md)
- [Quy tắc tiền xử lý](docs/preprocessing.md)
- [Chia tập và TF-IDF](docs/vectorization.md)
- [Câu hỏi vấn đáp và thực hành](docs/viva_questions.md)
- [Kế hoạch và nhật ký tiến độ](docs/PROGRESS.md)
