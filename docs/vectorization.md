# Chia dữ liệu và TF-IDF

## Chiến lược chia

Nếu nguồn có sẵn Train/Validation/Test, dùng `use_official_splits` để giữ nguyên từng tập và xác minh hai cột đã chỉ định. Nếu không có split chính thức, `stratified_holdout` chia Train, Validation và Test theo nhãn với `random_state=42` mặc định. Hàm báo lỗi nếu nhãn thiếu hoặc số mẫu không đủ để phân tầng; không tự ý xóa mẫu.

Trước khi biến đổi dữ liệu, gọi `assert_no_cross_split_duplicates` để đếm các nội dung trùng giữa từng cặp split. Quy tắc chuẩn hóa để so sánh là Unicode NFC, gộp khoảng trắng và không phân biệt hoa/thường; dấu câu và emoji vẫn được giữ. Hàm báo lỗi nếu phát hiện trùng để nhóm xem xét dựa trên quy định của nguồn, không âm thầm loại bản ghi.

## Tách từ tiếng Việt

`vietnamese_word_tokenize` dùng PyVi (`ViTokenizer`) để gộp các âm tiết thành từ tiếng Việt. PyVi mô tả API này trong [trang PyPI](https://pypi.org/project/pyvi/) và [repository chính thức](https://github.com/trungtv/pyvi). Có thể truyền một tokenizer khác khi cần kiểm tra hoặc so sánh cách tách từ.

## Biểu diễn đặc trưng

`fit_tfidf_on_train` tạo hai không gian đặc trưng:

- TF-IDF n-gram từ (mặc định unigram và bigram) sau tách từ tiếng Việt.
- TF-IDF n-gram ký tự (mặc định độ dài 2–5 ký tự).

Mỗi vectorizer chỉ được `fit_transform` trên Train. Validation và Test chỉ đi qua `transform`; hai ma trận được ghép thành ma trận thưa. Hàm trả các nhãn theo đúng thứ tự từng split và lưu cả hai vectorizer để kiểm tra kích thước/từ vựng. Không có mô hình phân loại nào được huấn luyện.

Các kiểm thử xác nhận từ/ngram chỉ có trong Validation/Test không xuất hiện trong từ vựng đã fit, số hàng đặc trưng khớp số nhãn và việc chia có thể tái tạo. Đây là kiểm thử quy trình trên fixture nhỏ, chưa thay thế việc xác minh các split ViHSD thật.
