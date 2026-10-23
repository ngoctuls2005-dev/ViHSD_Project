# Câu hỏi gợi ý cho vấn đáp Bài kiểm tra 1

Các câu trả lời dưới đây là gợi ý để tự học. Sinh viên cần diễn đạt lại bằng lời của mình và thay phần chưa có số liệu bằng kết quả đo thật; không học thuộc số liệu của fixture.

## Câu hỏi và gợi ý trả lời

1. **Bài toán thuộc loại nào? Mẫu, đầu vào và đầu ra là gì?**
   Gợi ý: phân loại văn bản đa lớp có giám sát; một mẫu là một bình luận tiếng Việt; đầu vào là văn bản được biểu diễn bằng đặc trưng đã chọn; đầu ra là `CLEAN`, `OFFENSIVE` hoặc `HATE`.

2. **Vì sao F1 Macro phù hợp hơn Accuracy đơn lẻ?**
   Gợi ý: F1 Macro tính F1 từng lớp rồi lấy trung bình đều; Accuracy có thể cao khi lớp đông được dự đoán tốt dù lớp ít mẫu bị bỏ sót. Cần nêu phân bố nhãn thực tế trước khi kết luận dữ liệu mất cân bằng.

3. **Train, Validation và Test khác nhau thế nào?**
   Gợi ý: Train dùng để học mô hình và khớp vectorizer; Validation dùng để chọn phương án trong lúc phát triển; Test chỉ dùng đánh giá cuối, không dùng để quyết định tham số.

4. **Vì sao giữ split chính thức hoặc chia phân tầng?**
   Gợi ý: split chính thức giữ cách chia mà bộ dữ liệu cung cấp; nếu tự chia, phân tầng giúp mỗi tập có tỷ lệ lớp gần với toàn bộ dữ liệu. Seed cố định giúp lặp lại kết quả. Quyết định của nhóm còn phải khớp schema và kích thước thật.

5. **Vì sao kiểm tra bình luận trùng giữa Train và Test?**
   Gợi ý: nếu cùng nội dung lọt vào cả hai tập, đánh giá có thể quá lạc quan vì Test không còn độc lập. Quy tắc so sánh và số lượng trùng phải được báo cáo.

6. **Tiền xử lý nào có thể làm mất thông tin?**
   Gợi ý: bỏ từ phủ định có thể đảo nghĩa; xóa dấu câu/emoji có thể làm mất sắc thái; sửa từ lóng quá mạnh có thể đổi nghĩa. Nên chuẩn hóa Unicode/khoảng trắng và chỉ mở rộng từ viết tắt theo từ điển có kiểm soát.

7. **Vì sao vectorizer chỉ được fit trên Train?**
   Gợi ý: từ vựng và trọng số IDF là thông tin được học từ dữ liệu. Nếu Test tham gia fit, quy trình đã nhìn trước dữ liệu đánh giá. Validation/Test chỉ được transform bằng vectorizer đã fit trên Train.

8. **Fixture trong kiểm thử chứng minh điều gì và không chứng minh điều gì?**
   Gợi ý: fixture giúp kiểm tra đường chạy, quy tắc Unicode, đếm và rò rỉ kỹ thuật. Nó không đại diện phân bố ViHSD, không chứng minh kết luận nghiên cứu và không thay cho quyền truy cập bộ dữ liệu thật.

## Thực hành tại chỗ

- Đổi một mục trong `DEFAULT_ABBREVIATIONS`, chạy lại cell tiền xử lý và đọc số dòng thay đổi.
- Đếm nhãn hoặc độ dài lại với một hàm khác trong notebook.
- Vẽ lại biểu đồ, đặt tiêu đề/trục và giải thích dựa trên số liệu vừa tạo.
- Nêu rõ notebook đang ở chế độ fixture hay CSV cục bộ trước khi diễn giải.
