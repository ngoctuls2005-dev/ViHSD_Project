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

## 3. Pipeline và CV

Pipeline: chuẩn hóa văn bản → PyVi → word TF-IDF n-gram `(1,2)` → classifier. Có chế độ bổ sung character TF-IDF `(2,5)`. Ma trận là sparse. Trong CV, bộ chuẩn hóa/TF-IDF được fit lại riêng ở train của fold; Validation và Test chính thức không tham gia fit.

| Cách chia CV | Fold | Seed | Nhóm trùng giao Train/validation mỗi fold (TB) | Macro F1 mean ± std của SVC |
|---|---:|---:|---:|---:|
| StratifiedKFold | 3 | 42 | 681,7 | 0,6262 ± 0,0049 |
| StratifiedGroupKFold | 3 | 42 | 0 | 0,6117 ± 0,0078 |

Train có 24.048 dòng, 22.500 nhóm khóa văn bản sau chuẩn hóa, 1.548 dòng lặp dư và 132 nhóm có nhiều nhãn. Group CV giữ các khóa trùng trong một fold, với phân bố lớp gần như bằng nhau giữa fold. StratifiedKFold có trung bình 681,7 nhóm xuất hiện ở cả phần fit và phần giữ lại mỗi fold; điểm của cách chia này có nguy cơ lạc quan.

## 4. Kết quả Validation

| Mô hình | Train Macro F1 | Validation Macro F1 | F1 CLEAN | F1 OFFENSIVE | F1 HATE |
|---|---:|---:|---:|---:|---:|
| Dummy majority | 0,3018 | 0,3003 | 0,9009 | 0,0000 | 0,0000 |
| MultinomialNB NumPy | 0,3118 | 0,3029 | 0,9012 | 0,0000 | 0,0074 |
| MultinomialNB scikit-learn | 0,3118 | 0,3029 | 0,9012 | 0,0000 | 0,0074 |
| Logistic Regression balanced | 0,9167 | 0,6049 | 0,8986 | 0,3948 | 0,5214 |
| Linear SVC balanced | 0,9831 | **0,6184** | 0,9339 | 0,3333 | 0,5878 |

Mô hình được khóa theo Validation là Linear SVC balanced, word TF-IDF 166.981 chiều, `C=1`. SVC có Train Macro F1 cao hơn Validation 0,3648; Logistic Regression chênh 0,3118. Đây là dấu hiệu khoảng cách fit đáng chú ý, nhưng không tự nó chứng minh nguyên nhân overfit. Macro F1 OFFENSIVE của SVC chỉ 0,3333; precision 0,5426 và recall 0,2406. Nhóm cần phân tích kỹ lớp này khi vấn đáp.

Lựa chọn `linear_svc_balanced` và Validation Macro F1 `0,6183585` đã được ghi vào `selection.json` trước khi chạy Test. Phân tích khoảng cách Train–Validation dựa trên các metrics đã tạo từ thực nghiệm.

## 5. Test và phép nhạy cảm

| Đánh giá sau khi khóa lựa chọn | Số dòng | Macro F1 | Accuracy | Ghi chú |
|---|---:|---:|---:|---|
| Test chính thức | 6.680 | 0,6017 | 0,8618 | Chấm một lần cho Linear SVC đã khóa |
| Bỏ dòng Test có khóa văn bản trong Train | 5.866 | 0,5926 | 0,8560 | Loại 814 dòng theo khóa văn bản; không dùng nhãn để tạo mask |

| Nhãn thật trên Test chính thức | Precision | Recall | F1 | Hỗ trợ |
|---|---:|---:|---:|---:|
| CLEAN | 0,9140 | 0,9488 | 0,9311 | 5.548 |
| OFFENSIVE | 0,4487 | 0,2365 | 0,3097 | 444 |
| HATE | 0,5648 | 0,5640 | 0,5644 | 688 |

Confusion matrix Test chính thức (hàng là nhãn thật, cột là dự đoán):

|  | Dự đoán CLEAN | Dự đoán OFFENSIVE | Dự đoán HATE |
|---|---:|---:|---:|
| Thật CLEAN | 5.264 | 81 | 203 |
| Thật OFFENSIVE | 243 | 105 | 96 |
| Thật HATE | 252 | 48 | 388 |

Lỗi phổ biến nhất ngoài đường chéo là HATE → CLEAN (252) và OFFENSIVE → CLEAN (243). Kết quả cho thấy recall OFFENSIVE còn thấp. Phép nhạy cảm có phân bố sau mask CLEAN 4.818, OFFENSIVE 403, HATE 645; giữ đây là phân tích phụ, không thay split Test chính thức.

Không ghi ví dụ bình luận, văn bản dự đoán theo dòng hoặc trọng số từ có thể lộ nội dung. Split chính thức có giao văn bản và xung đột nhãn đã báo ở báo cáo Tuần 4; phép nhạy cảm không thay Test chính thức.

## 6. Đối chiếu tiêu chí và tình trạng minh chứng

| Tiêu chí | Minh chứng kỹ thuật cần có | Trạng thái hiện tại |
|---|---|---|
| 1. Chọn thuật toán | Lý do phù hợp TF-IDF sparse, mất cân bằng, baseline | Có giải thích trong tài liệu; cần sinh viên tự trình bày |
| 2. Baseline | DummyClassifier chạy thật và metrics | Có kết quả Train/Validation; Macro F1 Validation 0,3003 |
| 3. Pipeline | Mã end-to-end, fit trong fold | Có Pipeline và fold transformer; unit tests đạt |
| 4. Cài đặt Python | Script/Notebook chạy lại | Thực nghiệm dữ liệu thật đã tạo đủ kết quả CV, Validation, lựa chọn và Test; tiến trình chỉ thoát lỗi ở thông báo terminal cuối do encoding, sau đó đã sửa stdout. Vì Test đã được chấm một lần, chưa chạy lại toàn bộ script sau sửa; CLI, compile, kiểm thử và Notebook fixture đạt |
| 5. Huấn luyện/CV | Fold metrics, mean/std, Train chỉ dùng fit | Có 3-fold stratified và group trên Train, seed 42; grouped không giao group |
| 6. Đánh giá | Bảng metrics, confusion, so baseline | Có Validation/Test, metrics từng lớp và confusion matrix tổng hợp |
| 7. Phân tích lỗi | Train/Validation gap và cặp nhãn nhầm | Đã ghi chênh lệch và lỗi nhầm lớp, không đưa bình luận gốc |
| 8. Nguyên lý [CN] | Vấn đáp cá nhân | Chưa xác nhận |
| 9. Kết quả trên dữ liệu [CN] | Giải thích kết quả mô hình của nhóm | Chưa xác nhận |
| 10. Thực hành [CN] | Thao tác trực tiếp của từng sinh viên | Chưa xác nhận |

## 7. Tái lập và an toàn

Lệnh: `python scripts/run_exam2_experiments.py --features word --cv-folds 3`. Lần chạy ngày 2026-11-10 dùng Python 3.13, scikit-learn 1.9.0 và seed 42. Các bảng/biểu đồ/metadata tổng hợp ghi trong `reports/exam2_results/`; không ghi bình luận hay dự đoán theo dòng. Script đã hoàn tất fit, lựa chọn và chấm Test, sau đó gặp lỗi mã hóa chỉ ở thông báo terminal cuối; dữ liệu đầu ra đã được kiểm tra. Lỗi đầu ra console đã được sửa. Không chạy lại Test trong lượt này.

Kiểm thử cuối: `$env:MPLBACKEND='Agg'; $env:VIHSD_RUN_INTEGRATION='1'; python -m pytest -q tests` — **33 passed in 36.58s**. Bộ kiểm thử gồm kiểm thử tích hợp dữ liệu thật và chạy các cell Notebook trên fixture; kết quả này không thay cho việc Tú/Tài tự thao tác hoặc vấn đáp.

## 8. Giới hạn

- Văn bản lặp và xung đột nhãn có thể làm CV stratified/official Test lạc quan; grouped CV xử lý trùng chính xác theo khóa nhưng không xử lý ngữ nghĩa gần giống.
- Class weight và cấu hình ban đầu chưa được tìm kiếm; không gọi đây là tối ưu.
- Kết quả cá nhân cần được Tú/Tài tự chạy, giải thích và giảng viên đánh giá.
