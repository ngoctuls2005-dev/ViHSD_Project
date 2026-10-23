# Hướng dẫn giải thích cách đánh giá

Tài liệu này giúp sinh viên trình bày quyết định đánh giá bằng lời của mình. Ví dụ dưới đây chỉ là ví dụ minh họa nhỏ, không phải dữ liệu hay kết quả ViHSD.

## Hold-out và các tập dữ liệu

Hold-out là cách giữ riêng một phần dữ liệu để đánh giá mô hình trên những mẫu chưa dùng khi học. Một cách chia thường gặp là Train, Validation và Test:

- **Train**: dùng để học tham số mô hình và khớp các phép biến đổi như TF-IDF.
- **Validation**: dùng để so sánh lựa chọn thiết kế hoặc tham số trong quá trình phát triển.
- **Test**: chỉ dùng một lần ở bước đánh giá cuối; không dùng để chọn mô hình hay ngưỡng.

Ví dụ, nếu có 100 bình luận, ta có thể dành 70 bình luận cho Train, 15 cho Validation và 15 cho Test. Tỷ lệ này chỉ minh họa; tỷ lệ thật phải căn cứ vào kích thước, phân bố lớp và các tập chính thức của ViHSD. Nếu ViHSD cung cấp sẵn các tập, ưu tiên giữ nguyên chúng.

Với phân loại nhiều lớp, chia phân tầng giúp giữ tỷ lệ các nhãn gần giống nhau giữa các tập. Cần kiểm tra bản ghi trùng giữa các tập để tránh mô hình gặp lại cùng nội dung ở cả Train và Test. Mọi phép biến đổi cần học từ dữ liệu phải chỉ `fit` trên Train; Validation và Test chỉ được `transform`.

## Precision, Recall và F1

Xét riêng một lớp, chẳng hạn `HATE`:

- **Precision**: trong những bình luận mô hình dự đoán là `HATE`, có bao nhiêu bình luận đúng?
- **Recall**: trong những bình luận thật sự mang nhãn `HATE`, mô hình tìm được bao nhiêu?
- **F1**: trung bình điều hòa của Precision và Recall; điểm này thấp nếu một trong hai thấp.

Ví dụ minh họa: mô hình gắn nhãn `HATE` cho 10 bình luận, trong đó 8 bình luận đúng; bộ dữ liệu có tổng cộng 20 bình luận `HATE`. Khi đó Precision là 8/10 = 0,80, Recall là 8/20 = 0,40, và F1 xấp xỉ 0,53. Mô hình khá chính xác khi dự đoán `HATE`, nhưng còn bỏ sót nhiều bình luận thuộc lớp này.

## Vì sao dùng F1 Macro?

F1 Macro tính F1 riêng cho từng lớp rồi lấy trung bình cộng, không phụ thuộc số mẫu của lớp. Nếu ba lớp có F1 lần lượt là 0,90, 0,60 và 0,30 thì F1 Macro là 0,60. Đây là ví dụ số học minh họa.

Accuracy chỉ đếm tỷ lệ dự đoán đúng trên toàn bộ mẫu. Nếu một lớp chiếm đa số, mô hình đoán lớp đó cho mọi bình luận có thể có Accuracy tưởng như cao nhưng không nhận diện được các lớp còn lại. Vì vậy cần xem F1 Macro và Precision/Recall/F1 của từng lớp cùng với ma trận nhầm lẫn.

## Vì sao chọn cách chia hiện tại?

Trong dự án này, nhóm sẽ kiểm tra trước xem ViHSD có cung cấp sẵn Train/Validation/Test hay không. Nếu có, giữ các tập chính thức giúp kết quả so sánh nhất quán với cách dùng của bộ dữ liệu. Nếu không, nhóm sẽ tự chia có phân tầng theo nhãn, đặt `random_state` cố định và kiểm tra bản ghi trùng giữa các tập. Quyết định cuối cùng cùng tỷ lệ chia chỉ được ghi sau khi dữ liệu thực tế đã được đọc và thống kê.
