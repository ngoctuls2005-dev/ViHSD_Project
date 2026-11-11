# Nhật ký đóng góp cá nhân

Nhật ký phân biệt rõ phần thành viên tự báo cáo với phần Codex đối chiếu kỹ thuật. Tú và Tài đã gửi báo cáo chi tiết ngày 2026-10-29 và bản tự xác nhận thực hành Tuần 6 ngày 2026-11-11; số liệu thực nghiệm đã được tái lập trên Train/Validation. Việc ai trực tiếp thao tác, giải thích và vấn đáp vẫn được ghi là **tự xác nhận**, không phải quan sát độc lập hay xác nhận của giảng viên. Tệp công khai không ghi mã sinh viên, dữ liệu gốc hoặc bình luận thật.

Xem [bảng phân công chung](TEAM_ASSIGNMENTS.md) và các [bài thực hành](practical_exercises.md). Mỗi thành viên chịu trách nhiệm xác nhận nội dung phần của mình. Nhật ký ghi báo cáo của Tú theo đúng tư cách tự xác nhận; không suy diễn ngày thực hiện hoặc xác nhận độc lập.

## Hoàng Ngọc Tú

- **Nhiệm vụ được giao:** Tuần 4: tiêu chí 1–5, Bài thực hành 1 & 3; Tuần 6: tiêu chí 1–2, 6–7, Naive Bayes, baseline Dummy, phân tích lỗi confusion matrix và tổng hợp báo cáo.
- **Trạng thái:** Tú tự xác nhận đã hoàn thành bài thực hành Tuần 4 (ngày 2026-10-29) và bài thực hành 10–15 phút Tuần 6 (ngày 2026-11-11: đổi `alpha` Naive Bayes sang 0.5, giải thích baseline Dummy, phân tích lỗi confusion matrix và tự xác nhận khai báo AI ở mục 9 báo cáo). Phần vấn đáp/thực hành tại lớp chờ giảng viên đánh giá trực tiếp.
- **Ngày ghi nhận:** 2026-10-29 (Tuần 4) và 2026-11-11 (Tuần 6).
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
| 2026-11-11 | Bài thực hành Tuần 6 (EXAM2_START_HERE_TU.md) & Tiêu chí 1–2, 6–7 | Đổi `alpha` NumPy NB từ 1.0 sang 0.5; giải thích baseline Dummy; phân tích lỗi confusion matrix; xác nhận khai báo AI | Validation Macro F1 tăng từ 0,3029 lên 0,3127 (Train từ 0,3118 lên 0,4561; F1 HATE từ 0,0074 lên 0,0357). Dummy Macro F1 Validation = 0,3003 (Acc 81,96%). Lỗi phổ biến nhất: HATE → CLEAN (265 ca ở NB, 89 ca ở SVC) và OFFENSIVE → CLEAN (208 ca ở NB, 109 ca ở SVC). Đã tự xác nhận mục 9 báo cáo. | Kết quả chạy cell 1, 3, 5, 9 notebook `exam2_practice.ipynb`; bảng metrics và confusion matrix so sánh | Tú tự xác nhận; chờ GV đánh giá vấn đáp trực tiếp |

**Đối chiếu số liệu Tuần 6:** theo báo cáo tự xác nhận của Tú ngày 2026-11-11, cấu hình NumPy NB `alpha=0.5` được chạy trên Development. Codex tái lập trên đúng Train/Validation: alpha 1.0 đạt Train/Validation Macro F1 `0,3117893/0,3028625`; alpha 0.5 đạt `0,4560731/0,3126742`, với Validation F1 CLEAN/OFFENSIVE/HATE `0,9023083/0/0,0357143`. Confusion matrix alpha 0.5 có CLEAN→HATE 1, OFFENSIVE→CLEAN 208, OFFENSIVE→HATE 4, HATE→CLEAN 265; các ô còn lại trên đường chéo. Confusion matrix Validation SVC từ kết quả Development đã lưu khớp số Tú nêu: CLEAN `[2092,26,72]`, OFFENSIVE `[109,51,52]`, HATE `[89,17,164]` theo thứ tự cột CLEAN/OFFENSIVE/HATE. Đây là tái lập số học, không xác nhận độc lập người đã thao tác hoặc giải thích.

## Lê Quang Tài

- **Nhiệm vụ được giao:** Tuần 4: tiêu chí 6–8, Bài thực hành 2, 4, 5; Tuần 6: tiêu chí 3–5, Pipeline, `StratifiedGroupKFold`, đổi `C`/`class_weight`, kiểm tra CV mean/std, chống rò rỉ dữ liệu và kiểm thử tái lập.
- **Trạng thái:** Tài tự xác nhận đã hoàn thành bài thực hành Tuần 4 (ngày 2026-10-29) và bài thực hành 10–15 phút Tuần 6 (ngày 2026-11-11: lần theo Pipeline/CV chống rò rỉ, giải thích `StratifiedGroupKFold`, đổi `C=0.5` cho Linear SVC / Logistic Regression, giải thích CV mean/std và tự xác nhận khai báo AI ở mục 9 báo cáo). Phần vấn đáp/thực hành tại lớp chờ giảng viên đánh giá trực tiếp.
- **Ngày ghi nhận:** 2026-10-29 (Tuần 4) và 2026-11-11 (Tuần 6).
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
| 2026-11-11 | Bài thực hành Tuần 6 (EXAM2_START_HERE_TAI.md) & Tiêu chí 3–5 | Lần theo Pipeline và StratifiedGroupKFold; đổi `C` từ 1.0 sang 0.5 cho SVC và Logistic Regression; giải thích CV mean/std; xác nhận khai báo AI | Grouped CV Macro F1: Linear SVC là 0,6117 ± 0,0078 (C=1) và 0,6110 ± 0,0065 (C=0.5); Logistic Regression là 0,5935 ± 0,0081 (C=1) và 0,5815 ± 0,0062 (C=0.5). Mean là hiệu năng TB qua fold; std là độ biến thiên giữa các fold. Không chọn tham số theo Test. Đã tự xác nhận mục 9 báo cáo. | Kết quả chạy cell 7 notebook `exam2_practice.ipynb`; bảng so sánh CV 3-fold và Validation | Tài tự xác nhận; chờ GV đánh giá vấn đáp trực tiếp |

**Đối chiếu số liệu Tuần 6:** theo báo cáo tự xác nhận của Tài ngày 2026-11-11, Codex tái lập các cấu hình `C=0.5` trên Train/Validation, dùng seed 42 và cùng split chính thức. Linear SVC: Stratified CV `0,6273107 ± 0,0049676`, Grouped CV `0,6109908 ± 0,0065381`, Validation Macro F1 `0,6134283`; Logistic Regression: lần lượt `0,5921789 ± 0,0013735`, `0,5814552 ± 0,0061574`, Validation `0,5883942`. Các số làm tròn khớp bảng tự báo cáo. Baseline `C=1.0` đối chiếu từ lượt Development đã lưu ngày 2026-11-10. Tái lập này xác minh khả năng lặp lại của kết quả; không xác nhận độc lập ai đã chạy hoặc giải thích.

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
