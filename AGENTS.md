# Quy tắc làm việc cho dự án ViHSD

## Mục tiêu và phạm vi

- Ưu tiên hoàn thành trung thực Bài kiểm tra 1 theo rubric của học phần.
- Thực hiện theo năm giai đoạn trong `docs/PROGRESS.md`; cập nhật trạng thái và bằng chứng sau mỗi giai đoạn.
- Không huấn luyện hoặc tối ưu mô hình trước khi tất cả tiêu chí Bài kiểm tra 1 hoàn tất và được kiểm chứng.
- Không tự nhận dự án đạt điểm tối đa; điểm do giảng viên đánh giá.

## Dữ liệu và tính trung thực

- Đọc schema, tên cột, mã nhãn và điều kiện sử dụng của dữ liệu thực tế trước khi viết giả định vào mã hoặc báo cáo.
- Không tạo dữ liệu giả rồi trình bày như dữ liệu ViHSD. Nếu nguồn dữ liệu không truy cập được, đánh dấu rõ phần chưa xác minh và chỉ dùng dữ liệu giả nhỏ cho kiểm thử kỹ thuật.
- Không đưa dữ liệu gốc, bình luận thật, thông tin cá nhân, token, khóa API hoặc tệp `.env` lên repository công khai.
- Không sửa nhãn gốc. Giữ dữ liệu đầu vào bất biến; lưu kết quả dẫn xuất ở vị trí riêng và loại khỏi Git nếu có nội dung bình luận thật.
- Trích dẫn nguồn và ghi lại cách tái tạo việc tải dữ liệu.

## Quy trình học máy

- Ưu tiên giữ các tập Train/Validation/Test chính thức nếu xác minh được.
- Nếu tự chia, dùng phân tầng khi phù hợp và cố định `random_state`.
- Chia dữ liệu trước mọi phép biến đổi có học thống kê. Chỉ `fit` vectorizer/biến đổi trên Train; chỉ `transform` Validation/Test.
- Không dùng Test để chọn đặc trưng, ngưỡng hoặc tham số.
- Dùng F1 Macro làm chỉ số chính đã định trước; báo cáo chỉ số từng lớp và giải thích ảnh hưởng của mất cân bằng.

## Mã và tài liệu

- Dùng đường dẫn tương đối, tương thích Windows và tránh cấu hình riêng máy cá nhân.
- Giữ module nhỏ, trách nhiệm rõ; tên hàm và biến dễ hiểu.
- Chú thích trong mã bằng tiếng Việt không dấu. README, báo cáo và hướng dẫn học tập bằng tiếng Việt có dấu.
- Cố định `random_state` ở nơi có yếu tố ngẫu nhiên.
- Nêu thư viện và lệnh chạy rõ ràng trong `requirements.txt`/README khi mã nguồn được thêm.
- Mọi biểu đồ, bảng và nhận xét định lượng phải được tạo từ dữ liệu đã kiểm chứng; không dùng số liệu minh họa như kết quả nghiên cứu.

## Kiểm thử và Git

- Viết và chạy kiểm thử phù hợp với chức năng của từng giai đoạn; ghi lệnh và kết quả thật trong `docs/PROGRESS.md`.
- Trước khi commit/push: xem `git status`, diff, kiểm tra tệp dữ liệu, notebook output và bí mật; không force push.
- Chỉ commit tệp mã nguồn/tài liệu an toàn và kết quả tổng hợp được phép chia sẻ.
- Thư mục giao nhiệm vụ `TEC/` là tài liệu làm việc cục bộ, không đưa vào repository công khai.
