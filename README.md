# ViHSD: Phát hiện ngôn từ thù ghét và xúc phạm

Dự án môn Học máy nghiên cứu phân loại bình luận mạng xã hội tiếng Việt thành ba nhãn: `CLEAN` (sạch), `OFFENSIVE` (xúc phạm) và `HATE` (thù ghét), sử dụng bộ dữ liệu ViHSD của UIT sau khi kiểm chứng cấu trúc và điều kiện sử dụng.

## Phạm vi hiện tại

Mốc đang thực hiện là **Bài kiểm tra 1 – tuần 4**. Trước tiên, nhóm xác định bài toán, khảo sát dữ liệu, xử lý chất lượng dữ liệu và chuẩn bị đặc trưng. Chưa huấn luyện mô hình cho đến khi hoàn tất các tiêu chí của Bài kiểm tra 1. Không có kết quả thực nghiệm hay thống kê dữ liệu nào được công bố trong tài liệu khởi tạo này.

## Bài toán

- Loại bài toán: phân loại văn bản đa lớp có giám sát.
- Một mẫu: một bình luận.
- Đầu vào: nội dung bình luận tiếng Việt.
- Đầu ra: một trong ba nhãn `CLEAN`, `OFFENSIVE`, `HATE`.
- Chỉ số chính dự kiến: F1 Macro, nhằm xem xét công bằng hiệu quả trên cả lớp ít mẫu.

Diễn giải nhãn và tên cột sẽ được đối chiếu với tài liệu, mã hóa nhãn và dữ liệu thực tế trước khi phân tích. Nhóm không sửa nhãn gốc hoặc tạo dữ liệu giả để thay cho ViHSD.

## Nguồn dữ liệu

- [ViHSD trên Hugging Face](https://huggingface.co/datasets/uitnlp/vihsd)
- [Mã nguồn ViHSD của nhóm tác giả](https://github.com/sonlam1102/vihsd)

Thẻ Hugging Face mô tả khoảng 33 nghìn bình luận và có các tập `train`, `validation`, `test`, nhưng yêu cầu chấp thuận điều kiện và chia sẻ thông tin tài khoản để xem tệp. Trang này ghi metadata giấy phép MIT; README của nhóm tác giả lại ghi dữ liệu chỉ dùng cho nghiên cứu. Phạm vi quyền sử dụng/tái phân phối vì vậy cần được làm rõ. Không đưa dữ liệu gốc hay bình luận thật vào repository công khai khi chưa xác nhận quyền.

## Tài liệu

- [Phát biểu bài toán](docs/problem_statement.md)
- [Nguồn và cách truy cập dữ liệu](docs/data_access.md)
- [Giải thích cách đánh giá](docs/evaluation_guide.md)
- [Kế hoạch và nhật ký tiến độ](docs/PROGRESS.md)
- [Báo cáo Bài kiểm tra 1](reports/exam1_report.md)

## Các giai đoạn

1. Khởi tạo dự án và tài liệu bài toán.
2. Khảo sát, thống kê và phân tích dữ liệu thực tế.
3. Phát hiện và xử lý vấn đề chất lượng dữ liệu.
4. Chuẩn bị dữ liệu và TF-IDF, kiểm soát rò rỉ dữ liệu.
5. Hoàn thiện báo cáo, kiểm thử và chuẩn bị vấn đáp.

Xem `docs/PROGRESS.md` để biết đầu ra, tiêu chí hoàn thành và trạng thái từng giai đoạn. Hướng dẫn cài đặt môi trường và chạy EDA cơ bản nằm bên dưới.

## Môi trường phát triển

Yêu cầu Python 3.10 trở lên. Trên Windows PowerShell, tạo môi trường và cài thư viện:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Sau khi có quyền truy cập dữ liệu, hãy lưu CSV cục bộ trong `data/raw/` (thư mục này bị Git bỏ qua), kiểm tra tên cột trong tệp thật, rồi chạy EDA với đúng tên cột đã xác minh:

```powershell
python scripts/run_eda.py --input "data/raw/<tep_csv>" --text-column "<cot_van_ban>" --label-column "<cot_nhan>"
```

Thay phần trong dấu `<...>` bằng đường dẫn và tên cột thực tế; lệnh không mặc định schema. Kết quả được ghi vào `artifacts/eda/`, thư mục cục bộ bị Git bỏ qua. Không chia sẻ thư mục đó trước khi rà soát từ/cụm từ trích xuất để tránh công khai nội dung nhạy cảm.
