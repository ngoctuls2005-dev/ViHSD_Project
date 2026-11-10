# Ôn vấn đáp và thực hành – Bài kiểm tra 2

Các gợi ý là khung học tập, không phải câu trả lời thay sinh viên. Cần giải thích bằng kết quả và mã thực tế của nhóm sau khi chạy.

## Câu hỏi vấn đáp

1. ViHSD có đầu vào, nhãn và ba split nào? Mã nhãn được giữ ra sao?
2. Dummy majority khác Macro F1 tham chiếu lý thuyết của Tuần 4 như thế nào?
3. Phát biểu định lý Bayes và vai trò giả định độc lập có điều kiện trong Naive Bayes.
4. Laplace smoothing làm gì? `alpha=1` thay đổi xác suất đặc trưng thế nào?
5. Vì sao MultinomialNB nhận được TF-IDF không âm? Vì sao NumPy implementation không cần biến ma trận sparse thành dense?
6. Logistic Regression tối ưu điều gì? `C` và `class_weight="balanced"` có ý nghĩa gì?
7. Linear SVC tìm ranh giới nào? Vai trò của margin và `C` là gì?
8. Tại sao không chỉ báo Accuracy? Macro F1 phản ánh lớp OFFENSIVE/HATE ra sao?
9. Vì sao TF-IDF phải fit lại trong từng train fold? Điều gì rò rỉ nếu fit trước CV?
10. StratifiedKFold và StratifiedGroupKFold khác gì? Vì sao nhóm dùng cả hai?
11. Tại sao dùng Validation để chọn mô hình và chỉ chấm Test sau khi khóa lựa chọn?
12. Đọc một hàng confusion matrix: lớp nào bị nhầm sang lớp nào? Nêu giới hạn do 80 nhóm giao Train–Test có xung đột nhãn.
13. Chênh lệch Train–Validation Macro F1 gợi ý điều gì? Vì sao chưa đủ để kết luận overfit?
14. Vì sao PhoBERT là hướng nghiên cứu tiếp theo nhưng không được đưa vào lượt baseline Tuần 6?

## Năm bài thực hành ngắn

### Bài 1 – Đổi alpha của NB

**Yêu cầu:** Đổi `alpha` từ 1.0 sang 0.5 trên fixture hoặc Train/CV.

**Thao tác:** Sửa cấu hình NB, chạy lại cùng folds và seed.

**Giải thích:** Alpha tăng làm làm trơn mạnh hơn; so sánh Macro F1 từng lớp và không chọn bằng Test.

### Bài 2 – Đọc confusion matrix

**Yêu cầu:** Tìm ô nhầm lớn nhất ngoài đường chéo trên Validation.

**Thao tác:** Lọc các hàng trong `validation_confusion_matrix.csv` có `true_label != predicted_label`.

**Giải thích:** Nêu cặp lớp bị nhầm và vì sao tổng hợp này không cho phép trích bình luận gốc.

### Bài 3 – Thay `class_weight`

**Yêu cầu:** So sánh `balanced` với `None` cho Logistic Regression trên Validation.

**Thao tác:** Đổi một tham số, fit lại trên Train, chỉ đọc Validation.

**Giải thích:** Balanced tăng trọng số tương đối của lớp ít; kiểm tra precision/recall theo lớp và Macro F1.

### Bài 4 – Kiểm tra group split

**Yêu cầu:** Chứng minh các khóa văn bản trùng không đi qua cả train và validation trong grouped CV.

**Thao tác:** Đọc `cv_group_class_distribution.csv` và cột `duplicate_groups_crossing_fold`.

**Giải thích:** StratifiedGroupKFold giữ group; nó không giải quyết bản gần giống hoặc nhãn xung đột.

### Bài 5 – Thêm chỉ số

**Yêu cầu:** Thêm Macro Recall vào bảng đọc kết quả (không thay đổi cách chọn đã khai báo).

**Thao tác:** Dùng `classification_metrics` hoặc thêm phép tính trên Validation.

**Giải thích:** Nêu mối quan hệ giữa recall từng lớp và recall trung bình; không đọc nhãn Test để điều chỉnh mô hình.
