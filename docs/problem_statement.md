# Phát biểu bài toán ViHSD

## Câu hỏi nghiên cứu

> Với một bình luận mạng xã hội viết bằng tiếng Việt, có thể dự đoán bình luận thuộc lớp sạch, xúc phạm hay thù ghét bằng các đặc trưng văn bản như thế nào?

Đây là câu hỏi về phân loại văn bản có giám sát. Đơn vị quan sát là **một bình luận**; mỗi mẫu có nội dung bình luận làm đầu vào và một nhãn do bộ dữ liệu cung cấp làm mục tiêu dự đoán.

## Đầu vào, đặc trưng và đầu ra

| Thành phần | Mô tả |
|---|---|
| Đơn vị mẫu | Một bình luận mạng xã hội tiếng Việt |
| Đầu vào ban đầu | Chuỗi văn bản của bình luận, giữ nguyên bản gốc để đối chiếu |
| Đặc trưng dự kiến | TF-IDF của n-gram từ và n-gram ký tự; độ dài và dấu hiệu viết không chuẩn có thể khảo sát trước khi quyết định dùng |
| Đầu ra | Một trong ba nhãn `CLEAN`, `OFFENSIVE`, `HATE` |

Đặc trưng chỉ được quyết định sau khi đọc schema và khảo sát dữ liệu thật. Tên cột, kiểu dữ liệu, cách mã hóa nhãn và cách chia tập chưa được xác minh tại giai đoạn khởi tạo.

## Diễn giải nhãn

- `CLEAN`: bình luận được gán nhãn sạch.
- `OFFENSIVE`: bình luận được gán nhãn xúc phạm.
- `HATE`: bình luận được gán nhãn thù ghét.

Đây là diễn giải theo tên lớp trong yêu cầu dự án. Định nghĩa vận hành chính xác và mã số tương ứng sẽ được trích từ tài liệu nguồn ViHSD khi khảo sát. Nhóm giữ nguyên nhãn gốc và không tự gán lại nhãn dựa trên từ khóa.

## Mục tiêu

### Mục tiêu thực tế

Khảo sát khả năng hỗ trợ nhận diện bình luận có ngôn từ xúc phạm hoặc thù ghét. Đây là công cụ hỗ trợ nghiên cứu, không thay thế việc hiểu ngữ cảnh hoặc quyết định kiểm duyệt của con người.

### Mục tiêu học máy

Xây dựng quy trình phân loại đa lớp từ văn bản bình luận sang ba nhãn ViHSD. Ở Bài kiểm tra 1, mục tiêu là kiểm chứng dữ liệu, phân tích đặc trưng, xử lý chất lượng dữ liệu và chuẩn bị quy trình biến đổi có thể tái tạo; chưa huấn luyện mô hình.

## Tiêu chí thành công

F1 Macro là chỉ số chính dự kiến. Nó tính F1 cho từng lớp rồi lấy trung bình đều, nên lớp ít mẫu vẫn có trọng số như lớp nhiều mẫu. Điều này phù hợp hơn Accuracy đơn lẻ khi phân bố lớp mất cân bằng: mô hình dự đoán tốt lớp đa số nhưng bỏ sót lớp thiểu số vẫn có thể đạt Accuracy cao.

Mức tham chiếu cho giai đoạn mô hình sẽ được xác định sau khi xác minh các tập dữ liệu và phân bố nhãn. Nhóm sẽ so sánh với một baseline đơn giản (ví dụ dự đoán lớp đa số) và báo cáo F1 Macro cùng Precision/Recall từng lớp. Hiện chưa có kết quả huấn luyện hay con số mục tiêu định lượng; không có số liệu nào được suy đoán.

## Phạm vi và giới hạn

- Phạm vi hiện tại là Bài kiểm tra 1; chưa huấn luyện hoặc tối ưu mô hình.
- Mỉa mai, phủ định, từ lóng và ngữ cảnh ngoài bình luận có thể làm ranh giới nhãn khó xác định.
- Một mô hình dựa trên văn bản có thể nhầm lẫn giữa xúc phạm và thù ghét; lỗi cần được phân tích thay vì che giấu bằng một chỉ số tổng hợp.
- Nguồn công khai mô tả bộ dữ liệu nhưng tệp yêu cầu chấp thuận điều kiện truy cập; phạm vi quyền sử dụng cần được làm rõ trước khi xử lý hoặc chia sẻ dữ liệu.
