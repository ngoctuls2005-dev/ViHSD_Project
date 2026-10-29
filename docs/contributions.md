# Nhật ký đóng góp cá nhân

Nhật ký phân biệt rõ phần thành viên tự báo cáo với phần Codex đối chiếu kỹ thuật. Ngày 2026-10-29, Tú gửi báo cáo chi tiết về các bước đã làm, số liệu tự giải thích và kết quả kiểm thử; các kết quả kỹ thuật chính khớp với lần đối chiếu độc lập. Việc thực hành và trả lời vấn đáp của Tú vẫn được ghi là **tự xác nhận**, không phải quan sát độc lập hay xác nhận của giảng viên. Tài chưa xác nhận. Tệp công khai không ghi mã sinh viên, dữ liệu gốc hoặc bình luận thật.

Xem [bảng phân công chung](TEAM_ASSIGNMENTS.md) và các [bài thực hành](practical_exercises.md). Mỗi thành viên chịu trách nhiệm xác nhận nội dung phần của mình. Nhật ký ghi báo cáo của Tú theo đúng tư cách tự xác nhận; không suy diễn ngày thực hiện hoặc xác nhận độc lập.

## Hoàng Ngọc Tú

- **Nhiệm vụ được giao:** tiêu chí 1–5; phụ trách chính Bài thực hành 1 và 3; tự làm Bài 2, 4, 5 để hiểu phần của Tài.
- **Trạng thái:** Tú tự báo cáo đã hoàn thành các bài thực hành 1–5, chạy Notebook trên dữ liệu thật và ôn 8 câu vấn đáp ngày 2026-10-29. Đây là tự xác nhận; chưa có quan sát độc lập về phần trình bày miệng hoặc thực hành tại lớp.
- **Ngày ghi nhận:** 2026-10-29, ngày gửi báo cáo; không suy diễn đây là ngày thực hiện từng thao tác.
- **Kết quả Tú tự giải thích:** Phân bố lớp và baseline Macro F1 lý thuyết 0,301756; chênh lệch trung vị độ dài; số liệu trùng/xung đột; phép lọc nhạy cảm; PyVi/TF-IDF và ranh giới fit/transform; ảnh hưởng chuẩn hóa trên bản sao.
- **Bằng chứng do Tú cung cấp:** Báo cáo chi tiết trong tin nhắn ngày 2026-10-29, gồm revision dữ liệu, lệnh chạy, các số liệu tổng hợp và kết quả tự báo cáo 25 kiểm thử đạt. Không kèm dữ liệu gốc hay bình luận thật.
- **Đối chiếu kỹ thuật:** Codex tái lập số liệu chính trên dữ liệu ViHSD thật và chạy lại bộ kiểm thử tích hợp: 25 đạt. Đối chiếu này xác nhận tính hợp lý kỹ thuật, không chứng minh ai đã thao tác hoặc trả lời vấn đáp.
- **Xác nhận của thành viên:** Tú tự xác nhận hoàn thành; phần vấn đáp/thực hành tại chỗ chưa được người khác ghi nhận độc lập.

| Ngày ghi nhận | Tiêu chí/bài | Việc Tú tự báo cáo đã làm | Kết quả Tú tự giải thích | Bằng chứng do Tú cung cấp | Trạng thái |
|---|---|---|---|---|---|
| 2026-10-29 | Khởi tạo và tiêu chí 3–5 | Chuẩn bị môi trường; tải/xác minh ViHSD revision `88e81b36ca376867640dad9df295e0f7d499ab80`; chạy 6 code cell Notebook | Train/Validation/Test 24.048/2.672/6.680; phân bố nhãn và trung vị độ dài được nêu trong báo cáo | Báo cáo chi tiết của Tú; số liệu split/schema/nhãn được Codex đối chiếu | Tú tự xác nhận |
| 2026-10-29 | Bài 1, tiêu chí 2 | Tự tính baseline luôn dự đoán CLEAN | Macro F1 lý thuyết `0,301756 ≈ 0,302`, không phải kết quả mô hình | Báo cáo chi tiết; phép tính được Codex tính lại từ Train | Tú tự xác nhận; phép tính đã đối chiếu |
| 2026-10-29 | Bài 2, học chéo | Tự kiểm toán trùng Train–Test trước/sau chuẩn hóa | 792/797 chuỗi; 857/867 dòng Train; 809/814 dòng Test; 80 chuỗi xung đột; 96 cặp dòng khác nhãn | Báo cáo chi tiết; số tổng hợp khớp lần tái lập của Codex | Tú tự xác nhận; số liệu đã đối chiếu |
| 2026-10-29 | Bài 3 | Tự giải thích đánh giá nhạy cảm giữ nguyên Test chính thức và lọc theo khóa văn bản | Còn 5.866 dòng Test, 5.776 chuỗi duy nhất; nhãn không dùng để tạo mask | Báo cáo chi tiết; số lượng và thứ tự thao tác được Codex đối chiếu | Tú tự xác nhận; số liệu đã đối chiếu |
| 2026-10-29 | Bài 4, học chéo | Tự chạy PyVi và TF-IDF; kiểm tra nơi fit/transform | 166.981 chiều từ + 393.272 chiều ký tự; fit trên Train, chỉ transform Validation/Test | Báo cáo chi tiết; cấu hình và số chiều được Codex đối chiếu | Tú tự xác nhận; kỹ thuật đã đối chiếu |
| 2026-10-29 | Bài 5, học chéo | Tự thử chuẩn hóa trên bản sao, giữ nguyên nguồn và nhãn | Theo báo cáo, số dòng thay đổi với quy tắc mặc định: Train 2.921/24.046, Validation 336/2.672, Test 789/6.680; nêu giới hạn của chuẩn hóa | Báo cáo chi tiết; dữ liệu gốc không nằm trong báo cáo | Tú tự xác nhận; chưa có quan sát độc lập thao tác cá nhân |
| 2026-10-29 | Tiêu chí 9–10 và kiểm thử | Tự báo cáo đã trả lời 8 câu vấn đáp, chạy Notebook và hoàn thành 25 kiểm thử | Giải thích được các quyết định và số liệu nêu trong báo cáo | Báo cáo chi tiết; Codex chạy lại bộ tích hợp và nhận 25 đạt | Tú tự xác nhận; phần vấn đáp/thực hành tại chỗ chưa được chứng kiến độc lập |

## Lê Quang Tài

- **Nhiệm vụ được giao:** tiêu chí 6–8; phụ trách chính Bài thực hành 2, 4 và 5; tự làm Bài 1 và 3 để hiểu phần của Tú.
- **Trạng thái:** Chưa xác nhận hoàn thành.
- **Ngày tự thực hiện:** Chưa ghi nhận.
- **Kết quả tự thực hiện:** Chưa ghi nhận.
- **Bằng chứng:** Chưa cung cấp.
- **Xác nhận của thành viên:** Chưa có.

| Ngày | Tiêu chí/bài | Việc Tài tự làm | Kết quả Tài tự giải thích | Bằng chứng do Tài cung cấp | Xác nhận của Tài |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Hỗ trợ do Codex chuẩn bị và thực hiện

Codex đã chuẩn bị bảng phân công, hướng dẫn bắt đầu và bài thực hành để nhóm sử dụng. Đây là hỗ trợ cho dự án, **không phải bằng chứng Tú hoặc Tài đã tự chạy notebook, thực hành hay trả lời vấn đáp**.

### 2026-10-29 – Đối chiếu kỹ thuật báo cáo của Tú

- Codex chạy tuần tự sáu code cell của Notebook trên ViHSD thật; xác nhận Train 24.048, Validation 2.672, Test 6.680, bảng phân bố nhãn, hai biểu đồ và TF-IDF 560.253 chiều. Notebook gốc vẫn không lưu output.
- Codex tính lại baseline Macro F1 lý thuyết `0,301756 ≈ 0,302` từ Train; không huấn luyện hoặc dự đoán mô hình.
- Codex tái lập kiểm toán trùng Train–Test (792/797 chuỗi; 857/867 dòng Train; 809/814 dòng Test; 80 chuỗi xung đột; 96 cặp dòng khác nhãn) và phép nhạy cảm dùng khóa văn bản sau chuẩn hóa (5.866 dòng Test, 5.776 chuỗi duy nhất). Nhãn Test không dùng để chọn dòng.
- Codex xác nhận `fit_transform` chỉ ở Train, `transform` ở Validation/Test; thử quy tắc `{"ko": "không"}` trên bản sao Train (1.991/24.046 dòng không thiếu thay đổi) và kiểm tra Series nguồn không đổi.
- Đây là bằng chứng thao tác của Codex để đối chiếu kỹ thuật với báo cáo chi tiết Tú gửi cùng ngày. Kết quả khớp không thay thế phần tự xác nhận của Tú và không chứng minh độc lập nội dung vấn đáp. Không có xác nhận của Tài.

## Cách ghi nhận

1. Sinh viên tự ghi ngày, tiêu chí/bài, thao tác đã làm và kết quả mình hiểu được.
2. Dẫn tệp, lệnh hoặc ảnh chụp đã lược bỏ thông tin nhạy cảm. Không chụp hoặc gửi bình luận thật, token hay đường dẫn chứa thông tin cá nhân.
3. Để thành viên tự xác nhận dòng của mình. Commit chỉ chứng minh trạng thái tệp, không tự chứng minh ai đã thao tác.
4. Nếu chưa làm, để trạng thái **Chưa xác nhận hoàn thành**; không đánh dấu hoàn tất dựa trên phân công hoặc kết quả chung của nhóm.
