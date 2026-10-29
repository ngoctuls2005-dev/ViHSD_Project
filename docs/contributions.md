# Nhật ký đóng góp cá nhân

Nhật ký phân biệt rõ phần thành viên tự báo cáo với phần Codex đối chiếu kỹ thuật. Ngày 2026-10-29, Tú và Tài gửi báo cáo chi tiết về các bước đã làm, số liệu tự giải thích và kết quả kiểm thử; các kết quả kỹ thuật chính khớp với phép kiểm tra độc lập. Việc thực hành và vấn đáp của mỗi người vẫn được ghi là **tự xác nhận**, không phải quan sát độc lập hay xác nhận của giảng viên. Tệp công khai không ghi mã sinh viên, dữ liệu gốc hoặc bình luận thật.

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
- **Trạng thái:** Tài tự báo cáo đã hoàn thành lộ trình 10 bước, gồm Bài 2, 4, 5 được giao chính và học chéo Bài 1, 3; đã chạy Notebook và báo cáo 25 kiểm thử đạt. Đây là tự xác nhận; không có người quan sát độc lập phần thực hành/vấn đáp tại chỗ.
- **Ngày ghi nhận:** 2026-10-29, ngày gửi báo cáo; không suy diễn đây là ngày thực hiện từng thao tác.
- **Kết quả Tài tự giải thích:** Phân biệt số chuỗi giao, số dòng bị ảnh hưởng và cặp nhãn khác nhau; giải thích phần tăng giao nhau sau chuẩn hóa; nêu vì sao giữ dữ liệu/split gốc; chỉ ra nơi fit/transform và kích thước/độ thưa ma trận; tính baseline và đề xuất tập nhạy cảm.
- **Bằng chứng do Tài cung cấp:** Báo cáo chi tiết trong tin nhắn ngày 2026-10-29, gồm lệnh, bảng tổng hợp, giải thích và kết quả tự báo cáo 25 kiểm thử. Không kèm dữ liệu gốc hoặc bình luận thật.
- **Đối chiếu kỹ thuật:** Các bảng audit, chiều/NNZ TF-IDF, thống kê chuẩn hóa mặc định và lần thử `{"ko": "không"}` khớp với dữ liệu/tệp tổng hợp đã kiểm chứng. Bộ kiểm thử tích hợp đã được Codex chạy lại trước đó: 25 đạt. Đối chiếu không chứng minh ai đã thao tác hoặc trả lời vấn đáp.
- **Xác nhận của thành viên:** Tài tự xác nhận hoàn thành; chưa có ghi nhận độc lập về phần trình bày miệng/thực hành tại lớp.

| Ngày ghi nhận | Tiêu chí/bài | Việc Tài tự báo cáo đã làm | Kết quả Tài tự giải thích | Bằng chứng do Tài cung cấp | Trạng thái |
|---|---|---|---|---|---|
| 2026-10-29 | Khởi tạo, xác thực và tiêu chí 3–5 | Tạo môi trường, đăng nhập Hugging Face, nạp dữ liệu thật và chạy 6 code cell Notebook | Ba split 24.048/2.672/6.680, tổng 33.400; schema `free_text`/`label_id`, nhãn 0/1/2 | Báo cáo chi tiết của Tài; schema và kích thước khớp dữ liệu đã xác minh | Tài tự xác nhận |
| 2026-10-29 | Bài 2, tiêu chí 6 | Chạy audit trùng Train–Test, đọc số liệu tổng hợp và bóc tách theo nhãn | Trước/sau: 792/797 chuỗi; 857/867 dòng Train; 809/814 dòng Test; 80 xung đột; 96 cặp dòng khác nhãn. CLEAN 759/769 Train, 725/730 Test; số OFFENSIVE/HATE không đổi | Báo cáo chi tiết; `train_test_duplicate_audit.csv` khớp | Tài tự xác nhận; số liệu đã đối chiếu |
| 2026-10-29 | Bài 4, tiêu chí 8 | Đọc mã PyVi/TF-IDF và đối chiếu kích thước/NNZ | 560.253 chiều; NNZ 4.388.235/450.955/1.126.992; fit chỉ Train, transform Validation/Test | Báo cáo chi tiết; `tfidf_dimensions.csv` và mã nguồn khớp | Tài tự xác nhận; số liệu đã đối chiếu |
| 2026-10-29 | Bài 5, tiêu chí 7 | Thử `{"ko": "không"}` trên bản sao và đối chiếu với quy tắc mặc định | Thử riêng: 1.991/24.046 dòng, 1.185.168 → 1.183.749 ký tự; mặc định: 2.921/24.046 Train, 336/2.672 Validation, 789/6.680 Test | Báo cáo chi tiết; thống kê mặc định khớp `preprocessing_comparison.csv`; thử riêng đã được Codex tái lập | Tài tự xác nhận; số liệu đã đối chiếu |
| 2026-10-29 | Bài 1 và 3, học chéo | Tự tính baseline và trình bày phương án đánh giá nhạy cảm | Macro F1 lý thuyết `0,301756 ≈ 0,302`; tập nhạy cảm còn 5.866 dòng/5.776 chuỗi; nhãn Test không dùng để lọc | Báo cáo chi tiết; phép tính và số lượng đã đối chiếu | Tài tự xác nhận; kết quả kỹ thuật đã đối chiếu |
| 2026-10-29 | Kiểm thử và nhật ký | Tài báo cáo 25/25 kiểm thử và đã tích 10/10 bước trong hướng dẫn | Kết quả tự báo cáo: 25 đạt trong 24,23 giây | Báo cáo chi tiết; Codex đã chạy lại cùng bộ tích hợp và nhận 25 đạt | Tài tự xác nhận; không phải quan sát độc lập |

## Hỗ trợ do Codex chuẩn bị và thực hiện

Codex đã chuẩn bị bảng phân công, hướng dẫn bắt đầu và bài thực hành để nhóm sử dụng. Đây là hỗ trợ cho dự án, **không phải bằng chứng Tú hoặc Tài đã tự chạy notebook, thực hành hay trả lời vấn đáp**.

### 2026-10-29 – Đối chiếu kỹ thuật báo cáo của Tú

- Codex chạy tuần tự sáu code cell của Notebook trên ViHSD thật; xác nhận Train 24.048, Validation 2.672, Test 6.680, bảng phân bố nhãn, hai biểu đồ và TF-IDF 560.253 chiều. Notebook gốc vẫn không lưu output.
- Codex tính lại baseline Macro F1 lý thuyết `0,301756 ≈ 0,302` từ Train; không huấn luyện hoặc dự đoán mô hình.
- Codex tái lập kiểm toán trùng Train–Test (792/797 chuỗi; 857/867 dòng Train; 809/814 dòng Test; 80 chuỗi xung đột; 96 cặp dòng khác nhãn) và phép nhạy cảm dùng khóa văn bản sau chuẩn hóa (5.866 dòng Test, 5.776 chuỗi duy nhất). Nhãn Test không dùng để chọn dòng.
- Codex xác nhận `fit_transform` chỉ ở Train, `transform` ở Validation/Test; thử quy tắc `{"ko": "không"}` trên bản sao Train (1.991/24.046 dòng không thiếu thay đổi) và kiểm tra Series nguồn không đổi.
- Đây là bằng chứng thao tác của Codex để đối chiếu kỹ thuật với báo cáo chi tiết Tú gửi cùng ngày. Kết quả khớp không thay thế phần tự xác nhận của Tú và không chứng minh độc lập nội dung vấn đáp. Không có xác nhận của Tài.

### 2026-10-29 – Đối chiếu kỹ thuật báo cáo của Tài

- Bảng `train_test_duplicate_audit.csv` xác nhận 792/797 chuỗi giao; 857/867 dòng Train và 809/814 dòng Test bị ảnh hưởng; 80 chuỗi xung đột và 96 cặp dòng khác nhãn. Các dòng theo lớp mà Tài nêu cũng khớp bảng tổng hợp.
- Bảng `tfidf_dimensions.csv` xác nhận 166.981 đặc trưng từ, 393.272 đặc trưng ký tự và 560.253 chiều tổng hợp; NNZ của Train/Validation/Test lần lượt là 4.388.235/450.955/1.126.992. Mã fit Train, transform Validation/Test.
- `preprocessing_comparison.csv` xác nhận thống kê quy tắc mặc định. Lần thử riêng `{"ko": "không"}` trên bản sao Train đã được Codex tái lập ở lượt trước: 1.991/24.046 dòng thay đổi, ký tự 1.185.168 → 1.183.749; nguồn không đổi.
- Bộ kiểm thử tích hợp đã được chạy lại trong cùng môi trường dự án ở lượt trước: **25 passed**. Báo cáo của Tài nêu 24,23 giây; thời gian chạy của Codex khác và không dùng làm minh chứng ai thực hiện bài.
- Đây là đối chiếu kỹ thuật, không xác nhận độc lập người thao tác hoặc phần vấn đáp. Tài tự báo cáo đã hoàn thành; không có xác nhận của giảng viên.

## Cách ghi nhận

1. Sinh viên tự ghi ngày, tiêu chí/bài, thao tác đã làm và kết quả mình hiểu được.
2. Dẫn tệp, lệnh hoặc ảnh chụp đã lược bỏ thông tin nhạy cảm. Không chụp hoặc gửi bình luận thật, token hay đường dẫn chứa thông tin cá nhân.
3. Để thành viên tự xác nhận dòng của mình. Commit chỉ chứng minh trạng thái tệp, không tự chứng minh ai đã thao tác.
4. Nếu chưa làm, để trạng thái **Chưa xác nhận hoàn thành**; không đánh dấu hoàn tất dựa trên phân công hoặc kết quả chung của nhóm.
