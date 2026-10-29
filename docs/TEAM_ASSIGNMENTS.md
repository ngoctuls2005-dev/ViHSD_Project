# Phân công nhóm – Bài kiểm tra 1

## Mục tiêu

Hoàn thiện minh chứng cho Bài kiểm tra 1 (tuần 4): phát biểu bài toán, phân tích dữ liệu ViHSD thật, rà soát chất lượng và chuẩn bị TF-IDF. Bài này chưa yêu cầu huấn luyện mô hình. Dữ liệu gốc, bình luận thật và token không được đưa lên GitHub. Bản công khai ghi họ tên và nhiệm vụ; mã sinh viên không được đăng trong repository.

## Thành viên và trách nhiệm

| Thành viên | Phần phụ trách chính | Bài thực hành chính | Trạng thái cá nhân |
|---|---|---|---|
| Hoàng Ngọc Tú | Tiêu chí 1–5: phát biểu bài toán, mục tiêu, mô tả dữ liệu, thống kê, biểu đồ và quan hệ đặc trưng–nhãn | Bài 1 và 3; đồng thời tự làm Bài 2, 4, 5 để hiểu phần của Tài | Tú tự báo cáo hoàn thành ngày 2026-10-29; số liệu kỹ thuật chính đã đối chiếu. Phần vấn đáp/thực hành tại chỗ chưa được chứng kiến độc lập |
| Lê Quang Tài | Tiêu chí 6–8: chất lượng dữ liệu, trùng lặp, chuẩn hóa tiếng Việt và chuẩn bị TF-IDF | Bài 2, 4, 5; đồng thời tự làm Bài 1, 3 để hiểu phần của Tú | Chưa xác nhận hoàn thành |
| Cả hai | Tiêu chí cá nhân 9–10: giải thích cách đánh giá, F1 Macro, dữ liệu và thao tác trực tiếp trên Notebook | Cùng luyện vấn đáp và thực hành tại chỗ | Tú tự báo cáo đã hoàn thành; Tài chưa xác nhận. Chưa có ghi nhận độc lập về phần vấn đáp/thực hành tại chỗ của Tú |

Đây là nhiệm vụ chính thức được giao cho nhóm. Trạng thái cá nhân phân biệt tự xác nhận với đối chiếu độc lập; báo cáo và mã nguồn của nhóm không tự chứng minh ai đã thao tác. Tú đã gửi báo cáo chi tiết và tự xác nhận ngày 2026-10-29; kết quả kỹ thuật được đối chiếu riêng. Tài chưa gửi kết quả. Điểm và đánh giá cuối cùng thuộc giảng viên.

## Danh sách công việc và đầu ra cần nộp

| Người phụ trách | Công việc | Đầu ra hoặc bằng chứng cần có | Tiêu chí hoàn thành | Trạng thái |
|---|---|---|---|---|
| Tú | Nêu bài toán, đơn vị mẫu, đầu vào/đầu ra; giải thích F1 Macro và baseline lý thuyết | Giải thích bằng lời của mình; phép tính Bài 1 | Phân biệt rõ baseline lý thuyết 0,302 với kết quả mô hình | Tú tự báo cáo hoàn thành; phép tính đã đối chiếu |
| Tú | Trình bày schema, phân bố, biểu đồ và ít nhất ba quan sát có số liệu | Giải thích được các bảng/hình trong báo cáo; hoàn thành Bài 3 | Dùng số liệu thật, không kết luận quan hệ nhân quả từ tương quan mô tả | Tú tự báo cáo hoàn thành; số liệu chính đã đối chiếu |
| Tài | Giải thích thiếu, trùng, xung đột nhãn, ngoại lệ và rủi ro giao split | Hoàn thành Bài 2; nêu được số dòng/nhãn liên quan | Phân biệt số chuỗi, số dòng và số cặp nhãn; không sửa nhãn gốc | Chưa xác nhận hoàn thành |
| Tài | Giải thích giới hạn chuẩn hóa và so sánh trước/sau | Hoàn thành Bài 5 trên bản sao trong bộ nhớ | Nêu được thay đổi và giới hạn; không ghi đè dữ liệu gốc | Chưa xác nhận hoàn thành |
| Tài | Giải thích PyVi, TF-IDF, kích thước ma trận và nơi fit/transform | Hoàn thành Bài 4 và chỉ đúng mã trong `src/vihsd/preparation.py` | Fit chỉ trên Train; Validation/Test chỉ transform | Chưa xác nhận hoàn thành |
| Tú và Tài | Luyện vấn đáp và thao tác cá nhân | Từng người tự trả lời, chạy lại một thao tác và ghi nhật ký | Mỗi người tự giải thích được kết quả và thực hiện được thao tác được hỏi | Tú tự báo cáo hoàn thành; chưa có người chứng kiến độc lập. Tài chưa xác nhận |

Các kết quả nhóm đã xác minh: 33.400 bình luận (Train 24.048, Validation 2.672, Test 6.680); baseline F1 Macro lý thuyết 0,3018; TF-IDF tổng 560.253 chiều; Train–Test có 792 chuỗi giao trước và 797 sau chuẩn hóa, 80 chuỗi xung đột nhãn. Xem [báo cáo](../reports/exam1_report.md) để biết số dòng bị ảnh hưởng và giới hạn của từng phép đo.

## Quy tắc phối hợp

1. Mỗi người tự chạy notebook, đọc phần được giao và ghi ngày, việc đã làm, kết quả giải thích được, bằng chứng và xác nhận vào [nhật ký đóng góp](contributions.md).
2. Hai người cùng xem phần của nhau: Tú tự làm Bài 2, 4, 5; Tài tự làm Bài 1, 3.
3. Không ghi tên người vào công việc chỉ dựa trên lịch sử Git hoặc thay đổi do Codex thực hiện.
4. Khi trao đổi kết quả, chỉ chia sẻ thống kê tổng hợp. Không gửi bình luận thật, dữ liệu gốc, token hoặc nội dung thư mục `artifacts/` lên GitHub.
5. Nếu một bước lỗi, ghi lệnh và thông báo lỗi đã lược bỏ thông tin nhạy cảm; không gửi token hoặc tệp dữ liệu.

## Hồ sơ liên quan

- [Hướng dẫn bắt đầu của Tú](START_HERE_TU.md)
- [Hướng dẫn bắt đầu của Tài](START_HERE_TAI.md)
- [Năm bài thực hành](practical_exercises.md)
- [Nhật ký đóng góp](contributions.md)
- [Báo cáo Bài kiểm tra 1](../reports/exam1_report.md)

