# Quy tắc tiền xử lý có kiểm soát

## Nguyên tắc

- Bản gốc không bị ghi đè; `normalize_series` tạo một Series mới.
- Chuẩn hóa Unicode về NFC và gộp khoảng trắng liên tiếp.
- Mở rộng một danh sách tường minh các từ viết tắt/teencode khi chúng chiếm trọn một token.
- Không tự sửa chính tả hay từ bị biến dạng chưa được xác minh.
- Không xóa phủ định, dấu câu hoặc emoji; các dấu hiệu này có thể mang thông tin.
- Quy tắc hiện tại đã được chạy trên ViHSD thật theo revision ghi trong báo cáo; số liệu dưới đây đo tác động, không chứng minh ngữ nghĩa của mọi cách viết.

## Từ điển viết tắt mặc định

`ko`, `khong`, `khum`, `k0` → `không`; `dc`, `đc` → `được`; `mik` → `mình`; `mn` → `mọi người`; `vs` → `với`.

Một số viết tắt có thể mơ hồ theo ngữ cảnh. Trong lần chạy thật, văn bản thay đổi là Train 2.921/24.046 dòng không thiếu (12,15%), Validation 336/2.672 (12,57%), Test 789/6.680 (11,81%). Bộ dò gồm các token trong từ điển giảm về 0 sau xử lý; đây chỉ là độ bao phủ của từ điển hữu hạn, không có nghĩa mọi teencode/từ né kiểm duyệt đã được phát hiện. Có thể truyền từ điển riêng vào `normalize_text` hoặc `normalize_series`; không có quy tắc nào thay nhãn.

Chuẩn hóa có thể nhập hai chuỗi khác nhau thành cùng một khóa. Theo dò NFC/khoảng trắng/không phân biệt hoa thường, giao Train–Test tăng từ 792 lên 797 chuỗi duy nhất; các dòng bị ảnh hưởng tăng 857→867 ở Train và 809→814 ở Test. Phép đo sau xử lý dùng nhãn Test chỉ để kiểm toán sự giao nhau/xung đột, không để chọn từ điển hoặc mô hình. Giữ bản gốc và báo cáo cả trước/sau.

## So sánh trước và sau

- `compare_text_versions` trả lại hai cột `original` và `processed` để xem cục bộ một số dòng.
- `preprocessing_summary` chỉ trả số dòng, số dòng thay đổi, tỷ lệ thay đổi và tổng số ký tự.
- Bảng đối chiếu có thể chứa bình luận thật. Không ghi bảng đó vào Git, notebook output công khai hay báo cáo; chỉ công bố thống kê tổng hợp sau khi rà soát quyền chia sẻ.

Kiểm thử xác nhận NFC, khoảng trắng, quy tắc token đầy đủ, giữ `không`, dấu câu, emoji, từ ngoài từ điển và tính bất biến của bản gốc trên fixture nhỏ. Chạy thật xác nhận quy trình và số dòng thay đổi; không chứng minh từng thay thế phù hợp về nghĩa. Vì vậy, kết quả chuẩn hóa được giữ ở bản dẫn xuất, không tự xóa các dòng trùng hoặc xung đột.
