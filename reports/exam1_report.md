# Báo cáo Bài kiểm tra 1 – ViHSD

> **Trạng thái:** bản nháp. Chỉ các mục có bằng chứng thực tế mới được xem là hoàn tất. Metadata nguồn đã xem nhưng dữ liệu không truy cập được trong phiên này; chưa có thống kê, biểu đồ hoặc kết quả mô hình ViHSD nào được tạo.

## 1. Phát biểu bài toán

Đây là bài toán phân loại văn bản đa lớp có giám sát. Một mẫu là một bình luận mạng xã hội tiếng Việt. Đầu vào là nội dung bình luận; đặc trưng dự kiến gồm TF-IDF n-gram từ và ký tự, sau khi kiểm chứng schema và khảo sát cách viết trong dữ liệu. Đầu ra là một trong ba nhãn `CLEAN` (sạch), `OFFENSIVE` (xúc phạm) và `HATE` (thù ghét). Tên cột và mã hóa nhãn sẽ được đối chiếu với dữ liệu và tài liệu nguồn; nhóm không tự thay đổi nhãn gốc.

## 2. Mục tiêu và tiêu chí thành công

Mục tiêu thực tế là khảo sát khả năng hỗ trợ nhận diện ngôn từ xúc phạm/thù ghét trong bình luận, không thay thế phán đoán theo ngữ cảnh của con người. Mục tiêu học máy là dự đoán ba nhãn ViHSD từ văn bản bình luận.

F1 Macro là chỉ số chính dự kiến vì tính F1 riêng cho từng lớp rồi lấy trung bình đều. Khi lớp mất cân bằng, Accuracy có thể bị chi phối bởi lớp đông và che khuất việc mô hình bỏ sót lớp ít mẫu. Giai đoạn mô hình sau này sẽ dùng baseline đơn giản (ví dụ dự đoán lớp đa số) làm mốc và báo cáo thêm Precision, Recall, F1 từng lớp cùng ma trận nhầm lẫn. Chưa xác định con số mục tiêu và chưa có kết quả huấn luyện; mức tham chiếu sẽ được quyết định sau khi xác minh các tập và phân bố dữ liệu.

## 3. Nguồn và mô tả dữ liệu

- Nguồn: [ViHSD trên Hugging Face](https://huggingface.co/datasets/uitnlp/vihsd) và [repository của nhóm tác giả](https://github.com/sonlam1102/vihsd). Thẻ Hugging Face mô tả khoảng 33 nghìn bình luận, ba nhãn `HATE`, `OFFENSIVE`, `CLEAN`, định dạng CSV và các tập `train`, `validation`, `test`; README tác giả nêu 33.400 bình luận.
- Tài liệu nghiên cứu: Luu, Son T.; Nguyen, Kiet Van; Nguyen, Ngan Luu-Thuy. (2021). “A Large-scale Dataset for Hate Speech Detection on Vietnamese Social Media Texts.” *IEA/AIE 2021*, tr. 415–426. [arXiv:2103.11528](https://arxiv.org/abs/2103.11528), [DOI](https://doi.org/10.1007/978-3-030-79457-6_35).
- Trang Hugging Face ghi metadata giấy phép MIT nhưng yêu cầu chấp thuận điều kiện/chia sẻ thông tin tài khoản để xem tệp. README của tác giả yêu cầu liên hệ để lấy dữ liệu và nói dữ liệu chỉ dùng cho nghiên cứu. Phạm vi áp dụng của giấy phép và quyền truy cập/tái phân phối chưa được làm rõ; chưa tải hay đọc nội dung dữ liệu.
- Tên cột, kiểu dữ liệu thực tế, số mẫu theo tập/lớp, điều kiện chi tiết, cách tải có thể tái tạo và từ điển dữ liệu: **chưa xác minh**, chờ quyền truy cập dữ liệu.
- Không đưa dữ liệu gốc hoặc bình luận thật vào repository công khai khi chưa xác nhận quyền.

## 4. Khảo sát thống kê và phân bố

**Chưa thực hiện.** Bảng thống kê, biểu đồ phân bố nhãn, độ dài, từ/cụm từ và dạng viết không chuẩn sẽ được tạo từ dữ liệu ViHSD đã xác minh. Không có hình hay nhận xét giả lập trong báo cáo.

## 5. Quan hệ đặc trưng với nhãn

**Chưa thực hiện.** Cần đo quan hệ giữa độ dài, từ/cụm từ, dạng viết bất thường và nhãn; sau đó ghi ít nhất ba nhận xét có căn cứ và hệ quả đối với tiền xử lý hoặc biểu diễn.

## 6. Vấn đề chất lượng dữ liệu

**Chưa thực hiện.** Sẽ định lượng dữ liệu thiếu/rỗng, trùng lặp, trùng khác nhãn, nhãn không hợp lệ, văn bản bất thường, teencode, ký tự lặp, mất cân bằng và nguy cơ rò rỉ. Bảng cần có số lượng, tỷ lệ và ví dụ an toàn.

## 7. Xử lý chất lượng dữ liệu

**Chưa thực hiện.** Sẽ mô tả quy tắc chuẩn hóa có kiểm soát, so sánh trước/sau, giữ phủ định và các dấu hiệu có thể mang thông tin, không sửa nhãn và không ghi đè dữ liệu gốc. Quy tắc phải có kiểm thử.

## 8. Chuẩn bị dữ liệu cho mô hình

Đã có mã giữ nguyên các split chính thức hoặc chia phân tầng với seed cố định, kiểm tra trùng giữa các split và tạo TF-IDF n-gram từ/ký tự. Mã chỉ `fit_transform` trên Train và chỉ `transform` Validation/Test; chưa huấn luyện mô hình. **Chưa chạy trên ViHSD thật** vì chưa truy cập được nội dung dữ liệu; kích thước split/ma trận và xác nhận không rò rỉ thực tế còn thiếu.

## 9. Phương pháp và chỉ số đánh giá

F1 Macro được chọn để phản ánh chất lượng trên cả ba lớp, kể cả lớp ít mẫu. Precision cho biết trong các mẫu dự đoán là một lớp có bao nhiêu mẫu đúng; Recall cho biết trong các mẫu thật sự thuộc lớp đó mô hình tìm được bao nhiêu; F1 cân bằng hai đại lượng. Accuracy đơn lẻ chưa đủ khi lớp mất cân bằng.

Nhóm sẽ giữ Train/Validation/Test chính thức nếu ViHSD cung cấp. Nếu phải tự chia, sẽ phân tầng theo nhãn khi phù hợp, cố định `random_state` và kiểm tra trùng giữa tập. Hold-out giữ riêng mẫu chưa dùng để đánh giá; Train dùng để khớp phép biến đổi và mô hình, Validation dùng cho quyết định phát triển, Test chỉ dùng đánh giá cuối. Giải thích minh họa đầy đủ có tại [`docs/evaluation_guide.md`](../docs/evaluation_guide.md). Tỷ lệ chia và kết quả cuối sẽ được ghi sau khi xác minh dữ liệu.

## Hạn chế, đóng góp và phạm vi dùng AI

- Hạn chế hiện tại: chưa kiểm tra điều kiện sử dụng hoặc nội dung thực tế của dữ liệu; chưa thể đưa ra nhận xét định lượng.
- Phân công và nhật ký đóng góp: sẽ bổ sung theo công việc thực tế của từng thành viên, không tự suy đoán.
- Phạm vi AI tạo sinh: hỗ trợ khởi tạo tài liệu, kế hoạch và giải thích học tập; nhóm cần rà soát, chạy lại mã và tự giải thích nội dung trước khi nộp.
