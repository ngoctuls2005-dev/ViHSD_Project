# Kế hoạch và nhật ký tiến độ

## Mục tiêu

Hoàn thành trung thực Bài kiểm tra 1 – tuần 4, gồm 10 tiêu chí, trước khi bắt đầu huấn luyện mô hình. Không khẳng định đạt điểm cụ thể; chỉ đánh dấu tiêu chí hoàn tất khi có sản phẩm và bằng chứng kiểm chứng được.

## Trạng thái tổng quan

- Repository: `ngoctuls2005-dev/ViHSD_Project`, nhánh chính `main`.
- Điểm bắt đầu: commit `2f3d61c707359c824921013813f484abcea9ca6c` (`Initial commit`), chỉ có README và `.gitignore`.
- Trạng thái dữ liệu: chưa tải/đọc nội dung ViHSD; trang Hugging Face yêu cầu chấp thuận điều kiện và chia sẻ thông tin tài khoản để truy cập tệp. Thẻ ghi metadata MIT, còn README của tác giả nói dữ liệu chỉ dùng cho nghiên cứu; phạm vi quyền sử dụng/tái phân phối chưa rõ.
- Trạng thái mô hình: chưa huấn luyện, đúng phạm vi Bài kiểm tra 1.
- Cập nhật gần nhất: 2026-10-23.

## Kế hoạch theo giai đoạn

### Giai đoạn 1 – Khởi tạo dự án và tài liệu bài toán

**Đầu ra:** quy tắc làm việc (`AGENTS.md`), README, phát biểu bài toán, giải thích phương pháp đánh giá, bộ khung báo cáo và kế hoạch theo giai đoạn.

**Điều kiện hoàn thành:** đầu vào/đầu ra và ba lớp được nêu cụ thể; F1 Macro được chọn và giải thích; không ghi kết quả giả; kế hoạch có đầu ra, tiêu chí hoàn thành và ranh giới rõ cho từng giai đoạn.

**Tiêu chí:** 1, 2 và bản hướng dẫn giải thích cho tiêu chí 9. **Trạng thái:** hoàn tất; tài liệu đã được rà soát thủ công. Chưa có mã thực thi ở giai đoạn này nên chưa có kiểm thử phần mềm để chạy.

### Giai đoạn 2 – Khảo sát và phân tích dữ liệu

**Đầu ra:** hướng dẫn tải/tái tạo; xác minh điều kiện sử dụng, schema, kiểu dữ liệu, nhãn và các tập; từ điển dữ liệu; mã EDA; bảng thống kê và biểu đồ có nhận xét dựa trên phép đo; ít nhất ba phân tích quan hệ đặc trưng–nhãn.

**Điều kiện hoàn thành:** số mẫu/cột/kiểu dữ liệu và phân bố nhãn được tạo từ dữ liệu thật; nguồn và giới hạn sử dụng được ghi rõ; biểu đồ có tiêu đề, nhãn trục và nhận xét cụ thể; không công khai bình luận thật trái điều kiện.

**Tiêu chí:** 3, 4, 5. **Trạng thái:** chưa bắt đầu; đã đọc metadata nguồn, cần tiếp tục xác minh quyền truy cập và lấy dữ liệu thật.

### Giai đoạn 3 – Phát hiện và xử lý chất lượng dữ liệu

**Đầu ra:** module phân tích vấn đề dữ liệu; module tiền xử lý có thể tái sử dụng; bảng trước/sau; unit test cho quy tắc chuẩn hóa.

**Điều kiện hoàn thành:** định lượng thiếu/rỗng, trùng, trùng khác nhãn, nhãn không hợp lệ, bất thường, teencode, ký tự lặp, mất cân bằng và rò rỉ; xử lý có kiểm soát, giữ phủ định/dấu câu/emoji có ý nghĩa, không sửa nhãn và không ghi đè bản gốc; có ví dụ an toàn.

**Tiêu chí:** 6, 7. **Trạng thái:** chưa bắt đầu.

### Giai đoạn 4 – Chuẩn bị dữ liệu và đặc trưng

**Đầu ra:** mã giữ tập chính thức hoặc chia phân tầng có seed; tách từ tiếng Việt; TF-IDF n-gram từ và ký tự; kiểm tra số mẫu, số chiều, nhãn và tính không rò rỉ.

**Điều kiện hoàn thành:** vectorizer chỉ `fit` trên Train, chỉ `transform` Validation/Test; không oversampling hay học thống kê trên toàn bộ dữ liệu; không dùng Test để chọn tham số/đặc trưng; có kiểm thử phù hợp.

**Tiêu chí:** 8. **Trạng thái:** chưa bắt đầu.

### Giai đoạn 5 – Báo cáo, kiểm thử và chuẩn bị vấn đáp

**Đầu ra:** báo cáo `reports/exam1_report.md` hoàn chỉnh cho tiêu chí 1–9; notebook thực hành; câu hỏi và trả lời gợi ý; hướng dẫn chạy trên Windows; bằng chứng kiểm thử và bảng đóng góp/nhật ký.

**Điều kiện hoàn thành:** notebook chạy lại từ đầu trên dữ liệu có quyền sử dụng; bảng, hình và số liệu được tạo từ kết quả thực tế; mọi giới hạn/chưa xác minh được nêu; sinh viên có thể giải thích và thao tác lại.

**Tiêu chí:** 9, 10 và hoàn thiện minh chứng cho 1–8. **Trạng thái:** chưa bắt đầu.

## Nhật ký tiến độ

### 2026-10-23 – Khởi tạo

- Đọc `TEC/Task.md` và `TEC/Evaluation_Criteria.md` trước khi lập kế hoạch.
- Kiểm tra repository công khai: nhánh `main` có một commit ban đầu, chưa có mã nguồn hay dữ liệu.
- Nối thư mục làm việc hiện có với repository; giữ thư mục `TEC/` cục bộ.
- Tạo quy tắc làm việc, tài liệu bài toán, hướng dẫn đánh giá, khung báo cáo và kế hoạch tiến độ. Chưa tải dữ liệu và chưa huấn luyện mô hình.
- Kiểm chứng giai đoạn: rà soát thủ công các tệp Markdown, liên kết nội bộ, trạng thái Git và việc không có dữ liệu dự án nào bị thêm.
- Kết quả kiểm thử phần mềm: chưa có mã thực thi ở giai đoạn này nên chưa có bộ kiểm thử phần mềm để chạy.
- Kiểm tra tài liệu: đạt; các tệp bắt buộc tồn tại, liên kết Markdown nội bộ đều tới tệp có thật, báo cáo có đủ mục 1–9 và kế hoạch có đủ năm giai đoạn.
- Kiểm tra Git: `git diff --cached --check` không phát hiện lỗi khoảng trắng; danh sách đưa vào commit chỉ gồm mã/tài liệu, không có `TEC/` hay dữ liệu.
- Commit/push: chuẩn bị thực hiện sau bước kiểm tra an toàn; SHA và trạng thái push được báo trong nhật ký bàn giao.

## Bằng chứng và quyết định chưa xác minh

- Thẻ [ViHSD trên Hugging Face](https://huggingface.co/datasets/uitnlp/vihsd) mô tả khoảng 33K bình luận có nhãn, các lớp `HATE`, `OFFENSIVE`, `CLEAN`, các tập `train`, `validation`, `test`, và metadata license MIT; tuy nhiên cần chấp thuận điều kiện/chia sẻ thông tin tài khoản để xem nội dung.
- README trong [repository của nhóm tác giả](https://github.com/sonlam1102/vihsd) nêu 33.400 bình luận, yêu cầu liên hệ để lấy dữ liệu, và ghi dữ liệu chỉ dùng cho nghiên cứu. Chưa xác minh được phạm vi áp dụng của metadata MIT so với lưu ý nghiên cứu; chưa đọc được nội dung dữ liệu, schema thực tế, số lượng theo tập/nhãn hoặc quyền tái phân phối. Không tải/chia sẻ dữ liệu khi chưa giải quyết điều kiện truy cập.
- Các tệp đầu vào giao nhiệm vụ trong `TEC/` được giữ cục bộ và loại khỏi repository công khai.
- Chưa có kết quả định lượng, biểu đồ hay kết luận EDA; các phần này chỉ được điền sau khi đọc dữ liệu thật.
