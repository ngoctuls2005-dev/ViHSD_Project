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
12. Đọc một hàng confusion matrix Validation: lớp nào bị nhầm sang lớp nào? Nêu giới hạn do văn bản lặp và nhóm có nhãn xung đột.
13. Chênh lệch Train–Validation Macro F1 gợi ý điều gì? Vì sao chưa đủ để kết luận overfit?
14. Vì sao PhoBERT là hướng nghiên cứu tiếp theo nhưng không được đưa vào lượt baseline Tuần 6?

## Năm bài thực hành ngắn

Tất cả bài chỉ dùng fixture hoặc Development (Train/CV/Validation); không nạp hay đọc nhãn Test. Mỗi bài dự kiến 10–15 phút.

### Bài 1 – Tú: thay `alpha` của Naive Bayes

**Yêu cầu:** Đổi `alpha` của `multinomial_nb_numpy` từ 1.0 thành 0.5.

**Thao tác:** Trong Notebook, gọi `estimators["multinomial_nb_numpy"].set_params(alpha=0.5)` trước khi chạy cell Validation; chạy lại cùng fixture hoặc cùng split Development.

**Giải thích:** `alpha` làm trơn số đếm đặc trưng; nêu chỉ số Validation Macro F1 và F1 từng lớp đã thay đổi ra sao, không kết luận từ một tham số đơn lẻ.

### Bài 2 – Tú: baseline và confusion matrix

**Yêu cầu:** Giải thích Dummy most-frequent và tìm một lỗi ngoài đường chéo của confusion matrix Validation.

**Thao tác:** Đọc hàng/cột của confusion matrix Validation, ghi tên nhãn và số lượng, không sao chép câu.

**Giải thích:** Phân biệt Accuracy cao do CLEAN chiếm đa số với Macro F1 ba lớp; mô tả ý nghĩa của một ô nhầm.

### Bài 3 – Tài: lần theo Pipeline và `StratifiedGroupKFold`

**Yêu cầu:** Chỉ ra điểm fit vectorizer và cách group văn bản trùng được giữ cùng fold.

**Thao tác:** Lần theo `cross_validate_text_models`; đối chiếu số group giao fold trong bảng CV Development hoặc fixture.

**Giải thích:** Vectorizer chỉ fit trong fold Train; grouped split ngăn trùng chính xác vượt fold nhưng không loại bản gần giống hay giải quyết nhãn xung đột.

### Bài 4 – Tài: thay `C` hoặc `class_weight`

**Yêu cầu:** Đổi đúng một tham số của Logistic Regression hoặc Linear SVC.

**Thao tác:** Dùng `set_params(C=0.5)` hoặc đổi `class_weight`, sau đó chạy lại CV trên Train và đánh giá Validation.

**Giải thích:** Mô tả thay đổi về Macro F1 và chỉ số theo lớp; giữ nguyên seed và dữ liệu để so sánh có ý nghĩa.

### Bài 5 – Tài: giải thích CV mean/std

**Yêu cầu:** So sánh mean và std Macro F1 của một mô hình giữa hai cách chia fold.

**Thao tác:** Đọc `cv_summary.csv` của một lượt Development hoặc tính `mean`/`std` từ `cv_folds.csv`.

**Giải thích:** Mean tóm tắt điểm trung bình theo fold; std cho biết độ dao động giữa fold, không phải khoảng tin cậy và không thay thế Validation.
