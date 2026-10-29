# Câu hỏi gợi ý cho vấn đáp Bài kiểm tra 1

Các gợi ý này dựa trên dữ liệu thật ở revision `88e81b36ca376867640dad9df295e0f7d499ab80`. Sinh viên cần tự chạy lại notebook, diễn đạt bằng lời của mình và giải thích giới hạn của từng con số. Không đọc bình luận thật ra ngoài báo cáo cục bộ được cấp quyền.

## Câu hỏi và gợi ý trả lời

1. **Bài toán, mẫu, đầu vào và đầu ra là gì?**
   Phân loại văn bản đa lớp có giám sát. Một mẫu là một bình luận; đầu vào là `free_text`; đầu ra là `label_id` với ba lớp `CLEAN`, `OFFENSIVE`, `HATE`. Mã gốc giữ nguyên.

2. **Vì sao dùng F1 Macro thay vì chỉ Accuracy?**
   Trong Train, CLEAN là 82,69%, OFFENSIVE 6,68%, HATE 10,63%; tỷ lệ CLEAN/OFFENSIVE là 12,38. Accuracy đơn lẻ có thể che khuất việc bỏ sót lớp ít mẫu. F1 Macro tính F1 của từng lớp với trọng số ngang nhau; cần báo cáo thêm chỉ số từng lớp.

3. **Điều gì khác nhau về độ dài giữa các lớp?**
   Trung vị ký tự của HATE là 59, còn CLEAN và OFFENSIVE là 31. Đây là xu hướng mô tả, không phải quy tắc nhãn; cần tránh kết luận một câu dài là HATE.

4. **Vì sao giữ split chính thức? Có vấn đề gì cần lưu ý?**
   Không tự chia lại khi nguồn cung cấp Train/Validation/Test. Tuy nhiên, 792 chuỗi chuẩn hóa trùng nhau giữa Train và Test; chuẩn hóa từ viết tắt làm con số này thành 797. Đây là nguy cơ làm đánh giá sau này lạc quan và phải được phân tích, không được bỏ qua.

5. **Vectorizer được học từ tập nào?**
   PyVi tách từ; TF-IDF từ dùng n-gram (1,2), TF-IDF ký tự dùng (2,5). Hai vectorizer chỉ fit trên Train; Validation và Test chỉ transform. Kích thước là 166.981 đặc trưng từ cộng 393.272 đặc trưng ký tự, tổng 560.253.

6. **Điều gì thay đổi sau chuẩn hóa?**
   Trong Train, 2.921/24.046 văn bản không thiếu thay đổi (12,15%). Quy tắc NFC, khoảng trắng và danh sách viết tắt hữu hạn tạo bản dẫn xuất; không sửa nhãn, không xóa dòng hay thay dữ liệu gốc. Hai văn bản thiếu được ghi nhận; vectorizer nhận chuỗi rỗng cho các dòng đó.

7. **Vì sao chưa xóa trùng, ngoại lệ hay ký tự lặp?**
   Trùng có thể mang nhãn xung đột; ngoại lệ độ dài có thể là bình luận thật; ký tự lặp và dấu câu/emoji có thể biểu đạt cường độ. Trước khi xóa hoặc sửa cần xem xét điều kiện sử dụng và tác động. Hiện chỉ thống kê và giữ nguyên dữ liệu nguồn.

8. **Các phân tích n-gram chứng minh điều gì?**
   Trong Train, 20 n-gram thiên về OFFENSIVE phủ 42,65% lớp này và 12,36% các lớp còn lại; nhóm thiên về HATE phủ 26,84% HATE và 1,46% lớp khác. Đây là mức độ bao phủ từ/cụm từ đã chọn, không phải độ chính xác hay quan hệ nhân quả; không được dùng Test để chọn các đặc trưng.

## Thực hành tại chỗ

- Chạy notebook từ đầu, nêu tỷ lệ ba nhãn trong Train và giải thích vì sao F1 Macro phù hợp.
- Thay tạm một quy tắc trong `DEFAULT_ABBREVIATIONS`, chạy lại trên bản sao và so sánh số dòng thay đổi; khôi phục quy tắc sau khi thử.
- Tính lại trùng Train–Test, giải thích cách chuẩn hóa dò trùng và vì sao không xóa tự động.
- In số mẫu và kích thước ma trận ba split; chỉ rõ lệnh nào fit và lệnh nào transform.
- Vẽ lại một biểu đồ với nhãn trục/tiêu đề phù hợp và đưa ra một nhận xét được số liệu hỗ trợ.
