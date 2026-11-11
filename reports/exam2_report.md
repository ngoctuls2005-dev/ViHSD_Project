# Báo cáo Bài kiểm tra 2 – ViHSD

> **Trạng thái:** đã chạy lượt thực nghiệm đầu trên dữ liệu ViHSD thật, revision `88e81b36ca376867640dad9df295e0f7d499ab80`. Đây là baseline Tuần 6, không phải tối ưu cuối. Điểm số do giảng viên đánh giá; tiêu chí cá nhân chưa được xác nhận thay cho sinh viên.

## 1. Mục tiêu và cách đánh giá

Phân loại bình luận tiếng Việt thành `CLEAN`, `OFFENSIVE`, `HATE`. Giữ split chính thức ViHSD: Train 24.048, Validation 2.672, Test 6.680 ở revision `88e81b36ca376867640dad9df295e0f7d499ab80`. Macro F1 là chỉ số chính; báo Precision, Recall, F1 từng lớp và confusion matrix do nhãn mất cân bằng.

## 2. Mô hình và cấu hình đầu tiên

| Mô hình | Tham số bắt đầu | Bằng chứng |
|---|---|---|
| Dummy most-frequent | dự đoán lớp thường gặp nhất | Đã chạy; Validation Macro F1 0,3003 |
| MultinomialNB NumPy | `alpha=1.0`, prior theo tần suất | Đã chạy; Validation Macro F1 0,3029 |
| MultinomialNB scikit-learn | `alpha=1.0` | Đã chạy; Validation Macro F1 0,3029 |
| Logistic Regression | `C=1`, `class_weight="balanced"`, `max_iter=1000` | Đã chạy; Validation Macro F1 0,6049 |
| Linear SVC | `C=1`, `class_weight="balanced"` | Đã chạy; Validation Macro F1 0,6184 |

Cấu hình khởi đầu chưa phải cấu hình tối ưu. Không dùng kết quả Test để thay đổi chúng. NumPy NB và scikit-learn NB cho cùng metrics ở mức lưu trong báo cáo; kiểm thử sparse đối chiếu xác suất và dự đoán trên fixture đạt.

### Baseline, khả năng khớp và giả thuyết về mô hình

**Bằng chứng đã quan sát trên lượt Validation đã lưu:** Dummy đạt Train/Validation Macro F1 `0,3018/0,3003`, với F1 OFFENSIVE và HATE bằng 0. Hai MultinomialNB đạt `0,3118/0,3029`; F1 OFFENSIVE bằng 0 và F1 HATE `0,0074`. Điểm thấp ngay trên Train và gần mức Validation cho thấy Dummy không phân biệt lớp thiểu số; NB với cấu hình ban đầu cũng chưa khớp tốt các lớp này. Đây là mô tả của các kết quả đã có, không phải kết luận về mọi cấu hình NB.

Linear SVC đạt Validation Macro F1 `0,6184`, cao hơn NB `0,3029`; Logistic Regression đạt `0,6049`. **Giả thuyết cần kiểm chứng thêm:** bộ phân loại tuyến tính có thể tận dụng ranh giới phân biệt trên TF-IDF nhiều chiều tốt hơn NB; đồng thời cấu hình tuyến tính hiện dùng `class_weight="balanced"`, còn NB không dùng cùng cơ chế cân bằng. Vì cấu hình không được thiết kế thành một thí nghiệm chỉ thay một yếu tố, số liệu hiện tại chưa chứng minh nguyên nhân nhân quả hay khẳng định mô hình tuyến tính luôn tốt hơn.

## 3. Pipeline và CV

Pipeline: chuẩn hóa văn bản → PyVi → word TF-IDF n-gram `(1,2)` → classifier. Có chế độ bổ sung character TF-IDF `(2,5)`. Ma trận là sparse. Trong CV, bộ chuẩn hóa/TF-IDF được fit lại riêng ở train của fold; Validation và Test chính thức không tham gia fit.

| Cách chia CV | Fold | Seed | Nhóm trùng giao Train/validation mỗi fold (TB) | Macro F1 mean ± std của SVC |
|---|---:|---:|---:|---:|
| StratifiedKFold | 3 | 42 | 681,7 | 0,6262 ± 0,0049 |
| StratifiedGroupKFold | 3 | 42 | 0 | 0,6117 ± 0,0078 |

Train có 24.048 dòng, 22.500 nhóm khóa văn bản sau chuẩn hóa, 1.548 dòng lặp dư và 132 nhóm có nhiều nhãn. Group CV giữ các khóa trùng trong một fold, với phân bố lớp gần như bằng nhau giữa fold. StratifiedKFold có trung bình 681,7 nhóm xuất hiện ở cả phần fit và phần giữ lại mỗi fold; điểm của cách chia này có nguy cơ lạc quan.

Biểu đồ CV trong thư mục kết quả đã công bố: [Macro F1 CV](exam2_results/cv_macro_f1.png), cùng [bảng mean/std CV](exam2_results/cv_summary.csv). Biểu đồ và bảng tóm tắt lượt thử đã ghi nhận; không phải kết quả sinh ra từ lần Development bảo vệ Test hiện tại.

## 4. Kết quả Validation

| Mô hình | Train Macro F1 | Validation Macro F1 | F1 CLEAN | F1 OFFENSIVE | F1 HATE |
|---|---:|---:|---:|---:|---:|
| Dummy majority | 0,3018 | 0,3003 | 0,9009 | 0,0000 | 0,0000 |
| MultinomialNB NumPy | 0,3118 | 0,3029 | 0,9012 | 0,0000 | 0,0074 |
| MultinomialNB scikit-learn | 0,3118 | 0,3029 | 0,9012 | 0,0000 | 0,0074 |
| Logistic Regression balanced | 0,9167 | 0,6049 | 0,8986 | 0,3948 | 0,5214 |
| Linear SVC balanced | 0,9831 | **0,6184** | 0,9339 | 0,3333 | 0,5878 |

Mô hình được khóa theo Validation là Linear SVC balanced, word TF-IDF 166.981 chiều, `C=1`. SVC có Train Macro F1 cao hơn Validation `0,3648` (`0,9831 − 0,6184`); Logistic Regression chênh `0,3118` (`0,9167 − 0,6049`). Đây là khoảng cách Train–Validation lớn, gợi ý khả năng khớp quá mức hoặc khác biệt độ khó giữa các split, nhưng chỉ hai con số này chưa xác định được nguyên nhân.

Validation Macro F1 cao nhất thuộc SVC: [biểu đồ Validation](exam2_results/validation_macro_f1.png), [bảng metrics](exam2_results/validation_model_metrics.csv) và [confusion matrix Validation](exam2_results/validation_confusion_matrix.csv). F1 OFFENSIVE của SVC là `0,3333`, precision `0,5426`, recall `0,2406`. Recall thấp nghĩa là mô hình chỉ tìm lại được khoảng 24% mẫu OFFENSIVE trong Validation; cân bằng lớp không đảm bảo recall cao. Lớp này có ít mẫu hơn CLEAN, nội dung có thể chồng lấn với lớp khác và ranh giới của cấu hình hiện tại có thể bỏ sót nhiều trường hợp. Đây là các khả năng cần kiểm tra thêm, không phải nguyên nhân đã được chứng minh.

Lựa chọn `linear_svc_balanced` và Validation Macro F1 `0,6183585` đã được ghi vào `selection.json` trước khi chạy Test. Phân tích khoảng cách Train–Validation dựa trên các metrics đã tạo từ thực nghiệm.

### Đặc trưng ảnh hưởng dự đoán

Chưa công bố bảng xếp hạng từ/cụm từ quan trọng vì các đặc trưng có thể trích lại nội dung nhạy cảm trong bình luận. Cách kiểm tra cục bộ: sau khi fit pipeline trên Train, lấy `get_feature_names_out()` từ TF-IDF và đối chiếu với `coef_` của Logistic Regression/Linear SVC (hoặc `feature_log_prob_` của MultinomialNB); xem đặc trưng có trọng số lớn cho từng lớp trong phiên làm việc riêng. Không lưu, commit, chụp màn hình hoặc đưa các từ/cụm từ hay bình luận ra tài liệu công khai. Notebook có hàm trợ giúp chỉ chạy khi người học chủ động gọi; mặc định không hiển thị đặc trưng.

## 5. Test và phép nhạy cảm

| Đánh giá sau khi khóa lựa chọn | Số dòng | Macro F1 | Accuracy | Ghi chú |
|---|---:|---:|---:|---|
| Test chính thức | 6.680 | 0,6017 | 0,8618 | Kết quả đã công bố từ lần chấm trước; không chạy lại trong lượt sửa an toàn này |
| Bỏ dòng Test có khóa văn bản trong Train | 5.866 | 0,5926 | 0,8560 | Loại 814 dòng theo khóa văn bản; không dùng nhãn để tạo mask |

| Nhãn thật trên Test chính thức | Precision | Recall | F1 | Hỗ trợ |
|---|---:|---:|---:|---:|
| CLEAN | 0,9140 | 0,9488 | 0,9311 | 5.548 |
| OFFENSIVE | 0,4487 | 0,2365 | 0,3097 | 444 |
| HATE | 0,5648 | 0,5640 | 0,5644 | 688 |

Confusion matrix Test chính thức đã lưu từ lần đánh giá trước (hàng là nhãn thật, cột là dự đoán; không chạy lại trong lượt sửa an toàn này):

|  | Dự đoán CLEAN | Dự đoán OFFENSIVE | Dự đoán HATE |
|---|---:|---:|---:|
| Thật CLEAN | 5.264 | 81 | 203 |
| Thật OFFENSIVE | 243 | 105 | 96 |
| Thật HATE | 252 | 48 | 388 |

Lỗi phổ biến nhất ngoài đường chéo là HATE → CLEAN (252) và OFFENSIVE → CLEAN (243). Kết quả đã lưu cho thấy recall OFFENSIVE trên Test là `0,2365` (105/444), phù hợp với vấn đề đã thấy trên Validation nhưng không được dùng để chọn tiền xử lý hoặc mô hình. Phép nhạy cảm có phân bố sau mask CLEAN 4.818, OFFENSIVE 403, HATE 645; giữ đây là phân tích phụ, không thay split Test chính thức. Xem [confusion matrix Test đã lưu](exam2_results/test_confusion_matrix.csv).

Không ghi ví dụ bình luận, văn bản dự đoán theo dòng hoặc trọng số từ có thể lộ nội dung. Split chính thức có giao văn bản và xung đột nhãn đã báo ở báo cáo Tuần 4; phép nhạy cảm không thay Test chính thức.

## 6. Đối chiếu tiêu chí và tình trạng minh chứng

| Tiêu chí | Minh chứng kỹ thuật cần có | Trạng thái hiện tại |
|---|---|---|
| 1. Chọn thuật toán | Lý do phù hợp TF-IDF sparse, mất cân bằng, baseline | Có giải thích trong tài liệu; cần sinh viên tự trình bày |
| 2. Baseline | DummyClassifier chạy thật và metrics | Có kết quả Train/Validation; Macro F1 Validation 0,3003 |
| 3. Pipeline | Mã end-to-end, fit trong fold | Có Pipeline và fold transformer; unit tests đạt |
| 4. Cài đặt Python | Script/Notebook chạy lại | Lượt thực nghiệm ban đầu và kết quả đã lưu trên dữ liệu thật được giữ nguyên. CLI Development đã chạy lại sau sửa encoding, chỉ dùng Train/CV/Validation; Test không được tải hoặc chấm trong lượt nghiệm thu này |
| 5. Huấn luyện/CV | Fold metrics, mean/std, Train chỉ dùng fit | Có 3-fold stratified và group trên Train, seed 42; grouped không giao group |
| 6. Đánh giá | Bảng metrics, confusion, so baseline | Có Validation/Test, metrics từng lớp và confusion matrix tổng hợp |
| 7. Phân tích lỗi | Train/Validation gap và cặp nhãn nhầm | Đã ghi chênh lệch và lỗi nhầm lớp, không đưa bình luận gốc |
| 8. Nguyên lý [CN] | Vấn đáp cá nhân | Chưa xác nhận |
| 9. Kết quả trên dữ liệu [CN] | Giải thích kết quả mô hình của nhóm | Chưa xác nhận |
| 10. Thực hành [CN] | Thao tác trực tiếp của từng sinh viên | Chưa xác nhận |

## 7. Tái lập và an toàn

Lệnh Development an toàn: `python scripts/run_exam2_experiments.py --mode development --features word --cv-folds 3`. Mặc định CLI cũng là Development. Lượt này chỉ yêu cầu split Train và Validation; kết quả ghi vào thư mục mới `reports/exam2_results/development/word/<run-id>/`, không ghi đè baseline đã công bố. `--features combined` có đường dẫn riêng. Chế độ `final-test` không mặc định, yêu cầu `--locked-config` đã chọn bằng Validation và ghi kết quả riêng. Không chạy chế độ này trong lượt sửa.

Ngày 2026-11-10, lệnh trên thoát mã `0` với dữ liệu thật revision `88e81b36ca376867640dad9df295e0f7d499ab80`: Train 24.048, Validation 2.672; CV 3 fold stratified và 3 fold grouped. Linear SVC được chọn bằng Validation Macro F1 `0,6183585`; CV Macro F1 mean/std là `0,6262 ± 0,0049` (stratified) và `0,6117 ± 0,0078` (grouped). [Manifest](exam2_results/development/word/acceptance-20261110/run_manifest.json), [metrics Validation](exam2_results/development/word/acceptance-20261110/validation_model_metrics.csv), [tóm tắt CV](exam2_results/development/word/acceptance-20261110/cv_summary.csv) và [cấu hình khóa đầy đủ](exam2_results/development/word/acceptance-20261110/selection.json). Manifest xác nhận `test_data_loaded=false` và `test_evaluated=false`; selection ghi snapshot tham số classifier.

Lượt ban đầu ngày 2026-11-10 đã fit, chọn và chấm Test một lần, rồi gặp lỗi mã hóa ở thông báo cuối; stdout đã được sửa. Bảng Test ban đầu tiếp tục được xem là kết quả lịch sử đã công bố, không được tái tạo trong nhiệm vụ này. Tệp Test đã kiểm tra bằng SHA-256 trước/sau.

Kiểm tra cuối ngày 2026-11-10: `python -m compileall -q src scripts tests` đạt; `$env:MPLBACKEND='Agg'; $env:VIHSD_RUN_INTEGRATION='1'; python -m pytest -q tests` — **42 passed, 5 subtests passed in 26.16s**. Bộ test xác minh dữ liệu thật, loader Development và Notebook Bài kiểm tra 1; Notebook Bài kiểm tra 2 đạt trên fixture và đã chạy riêng trên ViHSD thật chỉ với Train/Validation (30 fold results, chọn theo Validation). CLI Development bản cuối trên dữ liệu thật thoát mã `0`. Không chấm Test bằng mô hình trong lượt nghiệm thu này.

SHA-256 của các tệp Test/baseline đầu ra trước và sau đều trùng: `test_metrics.csv` `45A3B655CAA77DF23FC3AA800E33FA59CCC2C77C2A2C6D86FF7B4448318321B5`; `test_confusion_matrix.csv` `60305087146BD4CE622BDDB13678011580FA10888542A1F97B39AB177BAA207C`; `run_manifest.json` `F1198EE39798E91C83B0FBF5D19659211620ED9DC5A89E2C38AAC4FF1DDB51DA`; `selection.json` `08FA31A8F607436453FB48AB901EDC64F1C9086BB1683CF09E7EFFAB3B4310A8`.

## 8. Giới hạn

- Văn bản lặp và xung đột nhãn có thể làm CV stratified/official Test lạc quan; grouped CV xử lý trùng chính xác theo khóa nhưng không xử lý ngữ nghĩa gần giống.
- Class weight và cấu hình ban đầu chưa được tìm kiếm; không gọi đây là tối ưu.
- Kết quả cá nhân cần được Tú/Tài tự chạy, giải thích và giảng viên đánh giá.
- Chuẩn hóa hiện tại là tập quy tắc hữu hạn (Unicode NFC, khoảng trắng và từ điển viết tắt); không xử lý hết tiếng lóng, mỉa mai, lỗi chính tả hoặc tương đương ngữ nghĩa. Chuẩn hóa có thể làm giao Train–Test tăng từ 792 lên 797 chuỗi; không thể xem đó là thao tác trung tính.
- Bảng audit đã công bố ghi 792/797 chuỗi giao Train–Test trước/sau chuẩn hóa; tương ứng 857/867 dòng Train và 809/814 dòng Test bị ảnh hưởng. Có 80 nhóm chuỗi xung đột nhãn và 96 cặp dòng khác nhãn. Những con số này mô tả rủi ro của split chính thức; không dùng để chọn mô hình hoặc quy tắc chuẩn hóa trong lượt hiện tại.
- Kiểm thử xác nhận Development không nhận split Test và CV fit biến đổi trong fold; điều này không loại trừ mọi rò rỉ ngữ nghĩa hay rò rỉ từ quyết định thủ công. Split Test có trùng với Train vẫn được giữ nguyên để bảo toàn giao thức chính thức.

## 9. Khai báo sử dụng AI

Trong phạm vi lịch sử công việc đã ghi nhận cho dự án, **Codex GPT-6 Luna** đã hỗ trợ thiết kế quy trình, lập trình, kiểm thử, chạy thực nghiệm và soạn/chỉnh sửa tài liệu. Các kết quả thực nghiệm được nêu ở trên tạo từ dữ liệu ViHSD thật và các lệnh đã lưu; lượt sửa an toàn hiện tại chỉ chạy Development. AI không thay cho việc học, giải thích, thực hành cá nhân hoặc đánh giá của giảng viên.

**Xác nhận của thành viên nhóm (ngày 2026-11-11):**

Các dòng dưới đây ghi nhận nội dung tự xác nhận do nhóm gửi; đây không phải quan sát độc lập về thao tác hoặc vấn đáp.

- **Hoàng Ngọc Tú:** Đã đọc kỹ mục 9, tự thực hành bài tập Naive Bayes (`alpha=0.5`), kiểm chứng baseline Dummy và confusion matrix Validation, và tự xác nhận nội dung khai báo sử dụng AI này.
- **Lê Quang Tài:** Đã đọc kỹ mục 9, tự thực hành Pipeline, `StratifiedGroupKFold`, đổi tham số `C=0.5` cho Linear SVC / Logistic Regression, giải thích CV mean/std, và tự xác nhận nội dung khai báo sử dụng AI này.
*(Điểm số và đánh giá mức độ hiểu biết do giảng viên phụ trách học phần đánh giá trực tiếp qua buổi vấn đáp).*

## 10. Thực hành cá nhân Tuần 6 – tự báo cáo

Ngày 2026-11-11, Tú tự báo cáo đã đổi `alpha` NumPy NB từ `1.0` sang `0.5`, giải thích baseline và đọc confusion matrix Validation. Tài tự báo cáo đã lần theo Pipeline/grouped CV, đổi `C` của Linear SVC và Logistic Regression từ `1.0` sang `0.5`, giải thích CV mean/std. Các số dưới đây được Codex tái lập riêng trên Train/Validation của revision ghi ở mục 1; việc tự thao tác của từng người vẫn là tự xác nhận.

| Thực hành | Cấu hình | Train Macro F1 | Validation Macro F1 | Validation F1 (CLEAN / OFFENSIVE / HATE) |
|---|---|---:|---:|---:|
| Tú – NumPy NB | `alpha=1.0` | 0,3118 | 0,3029 | 0,9012 / 0 / 0,0074 |
| Tú – NumPy NB | `alpha=0.5` | 0,4561 | 0,3127 | 0,9023 / 0 / 0,0357 |
| Tài – Logistic Regression | `C=1.0` | 0,9167 | 0,6049 | 0,8986 / 0,3948 / 0,5214 |
| Tài – Logistic Regression | `C=0.5` | — | 0,5884 | 0,8853 / 0,3842 / 0,4956 |
| Tài – Linear SVC | `C=1.0` | 0,9831 | 0,6184 | 0,9339 / 0,3333 / 0,5878 |
| Tài – Linear SVC | `C=0.5` | — | 0,6134 | 0,9315 / 0,3333 / 0,5754 |

Với `alpha=0.5`, confusion matrix Validation của NB có OFFENSIVE→CLEAN 208, OFFENSIVE→HATE 4, HATE→CLEAN 265 và CLEAN→HATE 1. Confusion matrix SVC cấu hình `C=1.0` được liên kết ở mục 4. CV 3-fold của hai mô hình tuyến tính:

| Mô hình | C | Stratified Macro F1 mean ± std | Grouped Macro F1 mean ± std |
|---|---:|---:|---:|
| Linear SVC | 1,0 | 0,6262 ± 0,0050 | 0,6117 ± 0,0078 |
| Linear SVC | 0,5 | 0,6273 ± 0,0050 | 0,6110 ± 0,0065 |
| Logistic Regression | 1,0 | 0,6082 ± 0,0024 | 0,5935 ± 0,0081 |
| Logistic Regression | 0,5 | 0,5922 ± 0,0014 | 0,5815 ± 0,0062 |

Các giá trị `C=1.0` lấy từ lượt Development đã lưu ngày 2026-11-10; `C=0.5` được tái lập trên Train với seed 42. Bảng nhật ký có [chi tiết tự giải thích và nguồn tự báo cáo](../docs/contributions.md). Các lần thực hành này không nạp hoặc dùng nhãn Test để chọn tham số. Giảng viên vẫn cần đánh giá trực tiếp phần vấn đáp theo rubric.
