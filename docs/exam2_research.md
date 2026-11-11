# Nghiên cứu và lựa chọn phương pháp cho Bài kiểm tra 2

## Bài toán và dữ liệu

ViHSD là tập dữ liệu gán nhãn thủ công cho phát hiện bình luận CLEAN, OFFENSIVE và HATE. Bài báo gốc mô tả quá trình xây dựng/đánh giá dữ liệu và các thử nghiệm mạng nơ-ron, mô hình transformer. Nhóm dùng đúng dataset `uitnlp/vihsd` đã được cấp quyền, ba split chính thức và mã nhãn nguyên gốc. Kết quả của bài báo chỉ là bối cảnh nghiên cứu; không được coi là kết quả của nhóm hoặc so trực tiếp điểm số nếu điều kiện đánh giá khác.

## Vì sao dùng các mô hình này

| Phương pháp | Vai trò và lý do | Cấu hình đầu tiên |
|---|---|---|
| Dummy majority | Mốc thực nghiệm tối thiểu; cho biết mức đạt được khi chỉ dự đoán lớp phổ biến nhất | `strategy="most_frequent"` |
| MultinomialNB NumPy | Bài tập giải thích mô hình xác suất rời rạc; kiểm tra Laplace smoothing và thao tác sparse | `alpha=1.0`, prior theo tần suất lớp |
| MultinomialNB scikit-learn | Đối chứng độc lập để kiểm tra cài đặt NumPy | `alpha=1.0` |
| Logistic Regression | Mô hình tuyến tính xác suất với regularization; phù hợp ma trận TF-IDF sparse và đa lớp | `C=1`, L2 mặc định, `class_weight="balanced"` |
| Linear SVC | Mô hình tuyến tính tối đa hóa margin; thường hữu ích với dữ liệu văn bản nhiều chiều, thưa | `C=1`, `class_weight="balanced"` |

Cấu hình trên là baseline ban đầu, không phải siêu tham số tối ưu. Trọng số lớp cân bằng được bật trước cho hai mô hình tuyến tính do lớp không đều; NB vẫn giữ prior theo tần suất mặc định. Việc mở rộng sang ComplementNB hoặc feature combined chỉ thực hiện sau khi lượt đầu chạy ổn định và được ghi như thử nghiệm bổ sung, không phải tìm kiếm rộng.

## Pipeline và đánh giá

Pipeline gồm chuẩn hóa văn bản đã định nghĩa ở Tuần 4, PyVi segmentation cho word n-gram, TF-IDF `(1,2)` và classifier. Có chế độ `combined` thêm character n-gram `(2,5)`. Vectorizer được fit bên trong train của mỗi fold; chỉ transform phần giữ lại. Các ma trận được giữ ở dạng sparse.

Ba fold phân tầng trên Train cung cấp ước lượng ban đầu ổn định hơn một lần hold-out. Do dữ liệu có văn bản lặp, đánh giá theo `StratifiedGroupKFold` cũng được chạy khi khả thi. Kết quả grouped CV giảm khả năng một bình luận trùng xuất hiện cả ở train và validation của fold; nó không loại được các bản gần giống hoặc xung đột nhãn. Báo cáo cả hai cách chia và không diễn giải độ lệch chuẩn giữa fold như bất định thống kê đầy đủ.

Macro F1 là chỉ số chính vì tính F1 ngang trọng số giữa ba lớp. Kèm Precision/Recall/F1 từng lớp, Accuracy và confusion matrix. So sánh Train với Validation để xem dấu hiệu fit quá sát, nhưng điểm Train không đại diện khả năng khái quát. Chọn mô hình theo Validation; Test chính thức chỉ đọc sau khi lựa chọn đã khóa.

## Bối cảnh mô hình ngôn ngữ

PhoBERT là hướng phát triển dùng mô hình tiền huấn luyện tiếng Việt; công trình gốc và kho mã khuyến nghị đầu vào được word-segment trước theo tokenizer tương thích. ViSoBERT nghiên cứu văn bản mạng xã hội tiếng Việt và có thử nghiệm downstream hate-speech. Các mô hình này cần tài nguyên, quy trình fine-tuning và kiểm soát split riêng; chỉ nêu làm hướng sau, không huấn luyện trong lượt Tuần 6 này.

## Tài liệu tham khảo đã kiểm tra

1. Son T. Luu, Kiet Van Nguyen, Ngan Luu-Thuy Nguyen (2021). “A Large-scale Dataset for Hate Speech Detection on Vietnamese Social Media Texts.” IEA/AIE 2021, tr. 415–426. [Bài báo arXiv](https://arxiv.org/abs/2103.11528); [repository tác giả](https://github.com/sonlam1102/vihsd).
2. Nguyen, Dat Quoc and Anh Tuan Nguyen (2020). “PhoBERT: Pre-trained language models for Vietnamese.” Findings of EMNLP 2020. [ACL Anthology](https://aclanthology.org/2020.findings-emnlp.92/); [mã và hướng dẫn VinAI](https://github.com/VinAIResearch/PhoBERT).
3. Nam Nguyen, Thang Phan, Duc-Vu Nguyen, Kiet Nguyen (2023). “ViSoBERT: A Pre-Trained Language Model for Vietnamese Social Media Text Processing.” EMNLP 2023. [ACL Anthology](https://aclanthology.org/2023.emnlp-main.315/).
4. Tài liệu scikit-learn: [Multinomial Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html), [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), [LinearSVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html), [cross-validation và StratifiedGroupKFold](https://scikit-learn.org/stable/modules/cross_validation.html).

## Giới hạn nguồn

Đã đọc metadata và phần mô tả các nguồn trên; điểm số công bố của các nghiên cứu không được nhập vào bảng kết quả ViHSD của nhóm. Không có kết quả huấn luyện nào được ghi trong tài liệu này.
