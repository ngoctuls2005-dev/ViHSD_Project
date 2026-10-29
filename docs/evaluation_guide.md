# Hướng dẫn giải thích cách đánh giá

Tài liệu này giúp sinh viên trình bày quyết định đánh giá bằng lời của mình. Ví dụ dưới đây chỉ là ví dụ minh họa nhỏ, không phải dữ liệu hay kết quả ViHSD.

## Hold-out và các tập dữ liệu

Hold-out là cách giữ riêng một phần dữ liệu để đánh giá mô hình trên những mẫu chưa dùng khi học. Một cách chia thường gặp là Train, Validation và Test:

- **Train**: dùng để học tham số mô hình và khớp các phép biến đổi như TF-IDF.
- **Validation**: dùng để so sánh lựa chọn thiết kế hoặc tham số trong quá trình phát triển.
- **Test**: chỉ dùng một lần ở bước đánh giá cuối; không dùng để chọn mô hình hay ngưỡng.

Ví dụ, nếu có 100 bình luận, ta có thể dành 70 bình luận cho Train, 15 cho Validation và 15 cho Test. Tỷ lệ này chỉ minh họa; tỷ lệ thật phải căn cứ vào kích thước, phân bố lớp và các tập chính thức của ViHSD. Nếu ViHSD cung cấp sẵn các tập, ưu tiên giữ nguyên chúng.

ViHSD cung cấp Train/Validation/Test chính thức, nên dự án giữ các split đó. Kiểm tra thật tìm thấy 792 chuỗi chuẩn hóa giao nhau giữa Train–Test trước tiền xử lý và 797 sau; 857/809 dòng Train/Test bị ảnh hưởng trước, 867/814 sau. Có 80 chuỗi giao nhau có nhãn khác và 96 cặp dòng khác nhãn. Đây là rủi ro đánh giá đã được ghi trong báo cáo, không phải lý do để sửa split hoặc nhãn gốc.

Trong Bài kiểm tra 2, mọi phép biến đổi có học thống kê vẫn chỉ được `fit` trong phần Train của từng lần đánh giá. Mọi lựa chọn tiền xử lý/siêu tham số phải dùng Train/Validation. Sau khi khóa chúng, có thể báo cáo thêm phép nhạy cảm trên các chuỗi Test không giao với Train; giữ kết quả Test chính thức, báo số mẫu/lớp của tập con và không dùng kết quả Test để thay đổi lựa chọn.

## Precision, Recall và F1

Xét riêng một lớp, chẳng hạn `HATE`:

- **Precision**: trong những bình luận mô hình dự đoán là `HATE`, có bao nhiêu bình luận đúng?
- **Recall**: trong những bình luận thật sự mang nhãn `HATE`, mô hình tìm được bao nhiêu?
- **F1**: trung bình điều hòa của Precision và Recall; điểm này thấp nếu một trong hai thấp.

Ví dụ minh họa: mô hình gắn nhãn `HATE` cho 10 bình luận, trong đó 8 bình luận đúng; bộ dữ liệu có tổng cộng 20 bình luận `HATE`. Khi đó Precision là 8/10 = 0,80, Recall là 8/20 = 0,40, và F1 xấp xỉ 0,53. Mô hình khá chính xác khi dự đoán `HATE`, nhưng còn bỏ sót nhiều bình luận thuộc lớp này.

## Vì sao dùng F1 Macro?

F1 Macro tính F1 riêng cho từng lớp rồi lấy trung bình cộng, không phụ thuộc số mẫu của lớp. Nếu ba lớp có F1 lần lượt là 0,90, 0,60 và 0,30 thì F1 Macro là 0,60. Đây là ví dụ số học minh họa.

Accuracy chỉ đếm tỷ lệ dự đoán đúng trên toàn bộ mẫu. Nếu một lớp chiếm đa số, mô hình đoán lớp đó cho mọi bình luận có thể có Accuracy tưởng như cao nhưng không nhận diện được các lớp còn lại. Vì vậy cần xem F1 Macro và Precision/Recall/F1 của từng lớp cùng với ma trận nhầm lẫn.

### Mức tham chiếu lý thuyết từ Train

Trong ViHSD Train, CLEAN có 19.886/24.048 mẫu. Chiến lược hằng luôn dự đoán CLEAN có Precision CLEAN `19.886/24.048 = 0,8269`, Recall CLEAN `1`, F1 CLEAN `0,9053`, còn F1 OFFENSIVE và HATE bằng `0`. Macro F1 lý thuyết là `0,3018 ≈ 0,302`. Đây là phép tính từ phân bố lớp, **không phải kết quả huấn luyện hay đánh giá mô hình**. Dùng nó làm mốc cho Bài kiểm tra 2, không tự đặt một điểm mục tiêu cao hơn khi chưa chạy đánh giá hợp lệ.

## Vì sao giữ cách chia hiện tại?

Schema thật xác nhận ba split chính thức. Dự án giữ nguyên các split, đồng thời báo cáo số văn bản trùng và xung đột nhãn. Không chia lại trong Bài kiểm tra 1. Khi đánh giá Bài kiểm tra 2, có thể bổ sung phép chia theo nhóm văn bản chuẩn hóa trong dữ liệu phát triển và phép nhạy cảm trên phần Test không giao với Train, với quy trình lựa chọn đã khóa trước khi xem kết quả Test.
