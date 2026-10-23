# Quy tắc tiền xử lý có kiểm soát

## Nguyên tắc

- Bản gốc không bị ghi đè; `normalize_series` tạo một Series mới.
- Chuẩn hóa Unicode về NFC và gộp khoảng trắng liên tiếp.
- Mở rộng một danh sách tường minh các từ viết tắt/teencode khi chúng chiếm trọn một token.
- Không tự sửa chính tả hay từ bị biến dạng chưa được xác minh.
- Không xóa phủ định, dấu câu hoặc emoji; các dấu hiệu này có thể mang thông tin.
- Quy tắc hiện tại là khởi điểm kỹ thuật, chưa được đánh giá trên ViHSD thật.

## Từ điển viết tắt mặc định

`ko`, `khong`, `khum`, `k0` → `không`; `dc`, `đc` → `được`; `mik` → `mình`; `mn` → `mọi người`; `vs` → `với`.

Một số viết tắt có thể mơ hồ theo ngữ cảnh. Nhóm cần kiểm tra tần suất và ví dụ an toàn trên dữ liệu thật, sau đó chỉnh từ điển rõ ràng. Có thể truyền từ điển riêng vào `normalize_text` hoặc `normalize_series`; không có quy tắc nào thay nhãn.

## So sánh trước và sau

- `compare_text_versions` trả lại hai cột `original` và `processed` để xem cục bộ một số dòng.
- `preprocessing_summary` chỉ trả số dòng, số dòng thay đổi, tỷ lệ thay đổi và tổng số ký tự.
- Bảng đối chiếu có thể chứa bình luận thật. Không ghi bảng đó vào Git, notebook output công khai hay báo cáo; chỉ công bố thống kê tổng hợp sau khi rà soát quyền chia sẻ.

Kiểm thử hiện tại xác nhận NFC, khoảng trắng, quy tắc token đầy đủ, giữ `không`, dấu câu, emoji, từ ngoài từ điển và tính bất biến của bản gốc trên fixture nhỏ. Kết quả này là kiểm thử kỹ thuật, không chứng minh quy tắc phù hợp với toàn bộ ViHSD.
