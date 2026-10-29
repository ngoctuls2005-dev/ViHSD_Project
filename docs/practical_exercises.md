# Năm bài thực hành cá nhân – Bài kiểm tra 1

Các bài dưới đây dùng thống kê tổng hợp hoặc chạy trên dữ liệu cục bộ đã được cấp quyền. Không đưa bình luận thật vào ảnh chụp, báo cáo nộp công khai hoặc đầu ra Git. Chỉ giảng viên/sinh viên được giao mới xác nhận việc đã thực hành.

## Bài 1 – Tính mức tham chiếu F1 Macro

**Yêu cầu:** Tính bằng tay hoặc bằng một đoạn Python ngắn F1 Macro của chiến lược luôn dự đoán CLEAN từ phân bố Train.

**Thao tác:** Đọc số lượng Train trong báo cáo; tính Precision CLEAN = `19.886/24.048`, Recall CLEAN = `1`, F1 CLEAN = `2PR/(P+R)`. Gán F1 cho OFFENSIVE/HATE bằng `0`, rồi lấy trung bình ba lớp.

**Giải thích:** Kết quả xấp xỉ `0,302` là mức tham chiếu lý thuyết tính từ nhãn Train; không có mô hình nào được huấn luyện hay dự đoán. Nêu vì sao Accuracy của chiến lược này có thể trông cao nhưng Macro F1 thấp hơn.

## Bài 2 – Kiểm toán trùng Train–Test

**Yêu cầu:** Tái tạo số chuỗi giao nhau, số dòng bị ảnh hưởng và xung đột nhãn trước/sau chuẩn hóa.

**Thao tác:** Chạy `python scripts/run_real_dataset_analysis.py`; đọc `artifacts/real_vihsd/train_test_duplicate_audit.csv` tại máy cục bộ. Chỉ in các cột tổng hợp `stage`, số chuỗi, số dòng theo split/nhãn và số cặp nhãn khác; không mở hay in nội dung bình luận.

**Giải thích:** Trước xử lý có 792 chuỗi giao nhau, 857 dòng Train, 809 dòng Test, 80 chuỗi xung đột và 96 cặp dòng khác nhãn. Sau xử lý lần lượt là 797, 867, 814, 80 và 96. Nêu vì sao đây là rủi ro đánh giá và vì sao số chuỗi, số dòng, số cặp nhãn là ba đại lượng khác nhau.

## Bài 3 – Trình bày phương án đánh giá bổ sung

**Yêu cầu:** Viết quy trình cho Bài kiểm tra 2 để giảm ảnh hưởng của nội dung lặp mà vẫn giữ Test chính thức.

**Thao tác:** Nêu cách tạo nhóm bằng khóa văn bản NFC/khoảng trắng/không phân biệt hoa thường; dùng chia theo nhóm trong Train để chọn mô hình; khóa tiền xử lý và siêu tham số bằng dữ liệu phát triển; sau đó đánh giá trên Test chính thức và tập nhạy cảm được lọc chỉ theo khóa văn bản không giao Train–Test. Giữ các lặp/xung đột nội bộ Test trong phép nhạy cảm và báo riêng, không dùng nhãn Test để chọn dòng.

**Giải thích:** Phép nhạy cảm bổ sung không thay Test chính thức và không dùng kết quả Test để chọn mô hình. Báo rõ số dòng, số nhóm, phân bố nhãn và các xung đột còn lại. Con số hiện có là mô tả thiết kế, chưa phải kết quả mô hình.

## Bài 4 – Xác minh PyVi và TF-IDF

**Yêu cầu:** Giải thích vị trí fit/transform và đọc đúng số chiều của ba ma trận.

**Thao tác:** Chạy lại script; đọc `artifacts/real_vihsd/tfidf_dimensions.csv`; mở `src/vihsd/preparation.py` để tìm các lệnh `fit_transform` và `transform`. Không in từ vựng có thể chứa nội dung bình luận.

**Giải thích:** Train có 24.048 hàng; Validation 2.672; Test 6.680. Không gian từ có 166.981 chiều, ký tự 393.272, kết hợp 560.253. Vectorizer chỉ học từ Train; hai split còn lại dùng cùng từ điển/IDF đã fit.

## Bài 5 – Đánh giá giới hạn chuẩn hóa

**Yêu cầu:** Đo tác động của một quy tắc viết tắt đã có và giải thích rủi ro va chạm.

**Thao tác:** Dùng `normalize_series` và `preprocessing_summary` trên một bản sao dữ liệu; ghi số dòng thay đổi và số ký tự trước/sau. Không sửa `data/raw/`; không xuất văn bản trước/sau. Xem bảng giao nhau chỉ ở mức số liệu tổng hợp.

**Giải thích:** Trên Train, 2.921/24.046 văn bản không thiếu thay đổi. Chuẩn hóa làm Train–Test tăng từ 792 lên 797 chuỗi giao nhau; điều đó cho thấy quy tắc có thể nhập các dạng viết khác nhau thành một khóa. Không dùng nhãn Test hoặc kết quả Test để chọn quy tắc hay mô hình.

## Ghi nhận sau khi tự làm

Ghi ngày, tên sinh viên, bài đã thực hiện, kết quả đã giải thích và người xác nhận trong [`docs/contributions.md`](contributions.md). Tài liệu này không đánh dấu hoàn thành thay cho thao tác thật.
