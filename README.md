# ViHSD: Phát hiện ngôn từ thù ghét và xúc phạm

Dự án môn Học máy nghiên cứu phân loại bình luận mạng xã hội tiếng Việt thành `CLEAN`, `OFFENSIVE` và `HATE` bằng bộ dữ liệu ViHSD của UIT.

## HƯỚNG DẪN DÀNH CHO THÀNH VIÊN NHÓM

- [Hoàng Ngọc Tú – Bắt đầu tại đây](docs/START_HERE_TU.md)
- [Lê Quang Tài – Bắt đầu tại đây](docs/START_HERE_TAI.md)
- [Bảng phân công chung](docs/TEAM_ASSIGNMENTS.md)
- [Năm bài thực hành](docs/practical_exercises.md)
- [Nhật ký đóng góp cá nhân](docs/contributions.md)
- [Báo cáo Bài kiểm tra 1](reports/exam1_report.md)

## Trạng thái

Đang hoàn thành Bài kiểm tra 1 – tuần 4. Dữ liệu thật đã được tải và xác minh ở revision `88e81b36ca376867640dad9df295e0f7d499ab80`: 24.048 Train, 2.672 Validation và 6.680 Test. Báo cáo có thống kê, biểu đồ, kiểm tra chất lượng và TF-IDF thật. **Chưa huấn luyện mô hình**, đúng phạm vi bài kiểm tra. Kết quả chi tiết và các hạn chế nằm trong [báo cáo](reports/exam1_report.md) và [nhật ký tiến độ](docs/PROGRESS.md).

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

Không huấn luyện mô hình ở giai đoạn này. Không công khai `data/raw/`, các bảng chứa từ/cụm từ trích từ bình luận, hay notebook có output bình luận thật.

## Tài liệu dự án

- [Nguồn, quyền truy cập và tái tạo dữ liệu](docs/data_access.md)
- [Giải thích phương pháp đánh giá](docs/evaluation_guide.md)
- [Quy tắc tiền xử lý](docs/preprocessing.md)
- [Chia tập và TF-IDF](docs/vectorization.md)
- [Câu hỏi vấn đáp và thực hành](docs/viva_questions.md)
- [Kế hoạch và nhật ký tiến độ](docs/PROGRESS.md)
