# Chia dữ liệu và TF-IDF

## Chiến lược chia

Nếu nguồn có sẵn Train/Validation/Test, dùng `use_official_splits` để giữ nguyên từng tập và xác minh hai cột đã chỉ định. Nếu không có split chính thức, `stratified_holdout` chia Train, Validation và Test theo nhãn với `random_state=42` mặc định. Hàm báo lỗi nếu nhãn thiếu hoặc số mẫu không đủ để phân tầng; không tự ý xóa mẫu.

Ba split chính thức của ViHSD đã được xác minh: Train 24.048, Validation 2.672, Test 6.680. Kiểm toán tìm 322/792/92 chuỗi giao nhau ở Train–Validation/Train–Test/Validation–Test trước xử lý và 324/797/93 sau chuẩn hóa. `cross_split_duplicate_summary` đo phần giao; `assert_no_cross_split_duplicates` là guard cho tập dự kiến không giao nhau và sẽ báo lỗi trên các split ViHSD hiện tại. Không dùng lỗi đó để loại dòng hay chia lại dữ liệu nguồn.

Đối với Train–Test, 857 dòng Train và 809 dòng Test thuộc các chuỗi giao nhau trước xử lý; sau xử lý là 867 và 814. Có 80 chuỗi giao nhau có nhãn khác nhau, với 96 cặp dòng có nhãn mâu thuẫn. Các phép đo nhãn Test chỉ phục vụ kiểm tra chất lượng/rò rỉ; không dùng để quyết định từ điển, đặc trưng hay mô hình.

## Tách từ tiếng Việt

`vietnamese_word_tokenize` dùng PyVi (`ViTokenizer`) để gộp các âm tiết thành từ tiếng Việt. PyVi mô tả API này trong [trang PyPI](https://pypi.org/project/pyvi/) và [repository chính thức](https://github.com/trungtv/pyvi). Có thể truyền một tokenizer khác khi cần kiểm tra hoặc so sánh cách tách từ.

## Biểu diễn đặc trưng

`fit_tfidf_on_train` tạo hai không gian đặc trưng:

- TF-IDF n-gram từ (mặc định unigram và bigram) sau tách từ tiếng Việt.
- TF-IDF n-gram ký tự (mặc định độ dài 2–5 ký tự).

Mỗi vectorizer chỉ được `fit_transform` trên Train. Validation và Test chỉ đi qua `transform`; hai ma trận được ghép thành ma trận thưa. Hàm trả các nhãn theo đúng thứ tự từng split và lưu cả hai vectorizer để kiểm tra kích thước/từ vựng. Không có mô hình phân loại nào được huấn luyện.

Trên ViHSD thật, PyVi tạo 166.981 đặc trưng từ và TF-IDF ký tự tạo 393.272 đặc trưng; ma trận kết hợp có 560.253 chiều ở mỗi split. Vectorizer chỉ fit trên Train; Validation/Test chỉ transform. Kiểm thử fixture xác nhận token/ngram chỉ có ở Validation/Test không lọt vào từ vựng, còn kiểm thử tích hợp xác nhận schema/số hàng/nhãn trên revision thật. Nguy cơ lặp văn bản giữa split vẫn tồn tại trong nguồn và phải được nêu khi đánh giá mô hình.
