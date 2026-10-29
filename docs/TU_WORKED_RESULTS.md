# Kết quả làm việc phần Tú – bản hỗ trợ học tập

> Tài liệu này gom lời giải và cách giải thích cho phần Tú được giao, dựa trên số liệu tổng hợp đã ghi trong báo cáo dự án tại revision ViHSD `88e81b36ca376867640dad9df295e0f7d499ab80`. Đây là tài liệu hỗ trợ do Codex soạn, không phải xác nhận rằng Tú đã tự chạy Notebook, làm thực hành hay trả lời vấn đáp. Không chứa bình luận gốc hoặc dữ liệu cá nhân.

[Ảnh tóm tắt kết quả](TU_WORKED_RESULTS_PREVIEW.png)

## Phần chính của Tú: tiêu chí 1–5

### 1. Phát biểu bài toán

Đây là bài toán **phân loại văn bản đa lớp có giám sát**. Một mẫu là một bình luận mạng xã hội tiếng Việt.

- **Đầu vào:** nội dung bình luận ở cột `free_text`.
- **Đầu ra:** nhãn ở cột `label_id`: `0 = CLEAN`, `1 = OFFENSIVE`, `2 = HATE`.
- **Mục tiêu:** dự đoán nhãn của bình luận dựa trên nội dung. Nhãn gốc được giữ nguyên; nhóm không tự gán lại nhãn.
- **Giới hạn của Bài kiểm tra 1:** khảo sát dữ liệu và chuẩn bị đặc trưng; chưa huấn luyện bộ phân loại.

Câu trả lời ngắn khi thuyết trình: “Nhóm em phân loại mỗi bình luận tiếng Việt vào một trong ba nhãn CLEAN, OFFENSIVE và HATE. Đầu vào là văn bản, đầu ra là nhãn có sẵn trong bộ dữ liệu.”

### 2. Mục tiêu và chỉ số đánh giá

Nhóm chọn **F1 Macro** làm chỉ số chính. F1 Macro tính F1 riêng cho từng lớp rồi lấy trung bình đều, vì vậy lớp ít mẫu vẫn có trọng số ngang lớp đông. Cần xem thêm Precision, Recall và F1 từng lớp cùng ma trận nhầm lẫn; Accuracy một mình có thể che việc bỏ sót lớp thiểu số.

Mức tham chiếu lý thuyết nếu luôn đoán CLEAN, tính từ Train:

`Precision(CLEAN) = 19.886 / 24.048 = 0,826929`

`Recall(CLEAN) = 1`

`F1(CLEAN) = 2 × 0,826929 × 1 / (0,826929 + 1) = 0,905267`

Vì chiến lược này không bao giờ dự đoán OFFENSIVE hoặc HATE, F1 của hai lớp đó bằng 0:

`Macro F1 = (0,905267 + 0 + 0) / 3 = 0,301756 ≈ 0,302`

Accuracy của cách đoán này cũng là `19.886 / 24.048 = 82,69%`. Con số Accuracy trông cao nhưng hai lớp OFFENSIVE và HATE đều bị bỏ sót hoàn toàn. **0,302 là baseline tính từ tần suất nhãn Train, không phải kết quả mô hình**; Bài kiểm tra 1 chưa huấn luyện mô hình.

### 3. Nguồn và mô tả dữ liệu

Nguồn là bộ dữ liệu ViHSD `uitnlp/vihsd` của UIT NLP trên Hugging Face. Revision đã được nhóm ghi lại là `88e81b36ca376867640dad9df295e0f7d499ab80`. Nguồn yêu cầu đăng nhập và chấp thuận điều kiện truy cập. Do ghi chú sử dụng dữ liệu chưa được làm rõ hoàn toàn, dữ liệu gốc và bình luận thật được giữ ngoài GitHub; báo cáo công khai chỉ dùng số liệu tổng hợp.

| Split | Số mẫu | CLEAN | OFFENSIVE | HATE |
|---|---:|---:|---:|---:|
| Train | 24.048 | 19.886 (82,69%) | 1.606 (6,68%) | 2.556 (10,63%) |
| Validation | 2.672 | 2.190 (81,96%) | 212 (7,93%) | 270 (10,10%) |
| Test | 6.680 | 5.548 (83,05%) | 444 (6,65%) | 688 (10,30%) |
| **Tổng** | **33.400** | **27.624** | **2.262** | **3.514** |

Schema đã xác minh: `free_text` kiểu chuỗi và `label_id` kiểu số nguyên. Ánh xạ mã nhãn được dùng nhất quán là `0=CLEAN`, `1=OFFENSIVE`, `2=HATE`. Dữ liệu có ba split chính thức; nhóm giữ nguyên các split.

### 4. Thống kê và biểu đồ

![Phân bố nhãn ViHSD](../reports/figures/vihsd_label_distribution.png)

![Độ dài bình luận theo nhãn](../reports/figures/vihsd_comment_length_by_label.png)

Ba nhận xét có số liệu:

1. Train có 19.886 CLEAN nhưng chỉ 1.606 OFFENSIVE; lớp CLEAN đông gấp khoảng **12,38 lần** OFFENSIVE. Vì vậy cần báo cáo chỉ số riêng từng lớp.
2. Trung vị độ dài HATE là **59 ký tự**, trong khi CLEAN và OFFENSIVE đều là **31 ký tự**. Trung bình lần lượt là 84,17; 44,83; và 44,11 ký tự.
3. Số đơn vị cách nhau bằng khoảng trắng trung bình là 20,07 với HATE, 10,48 với CLEAN và 10,73 với OFFENSIVE. Đây chỉ là phép đếm khoảng trắng, **không phải** số từ tiếng Việt đã tách bằng PyVi.

Các biểu đồ và số liệu mô tả phân bố của tập dữ liệu. Chúng không chứng minh độ dài gây ra nhãn, cũng không tạo thành quy tắc “câu dài là HATE”.

### 5. Quan hệ giữa đặc trưng văn bản và nhãn

Các nhận xét dưới đây được tính trên Train và chỉ mô tả sự đồng xuất hiện:

- Một số dấu hiệu phủ định xuất hiện trong **16,90% HATE**, **9,40% CLEAN** và **7,97% OFFENSIVE**. Dấu hiệu phủ định có thể xuất hiện trong nhiều ngữ cảnh; riêng nó không xác định nhãn.
- Nhóm 20 n-gram thiên về OFFENSIVE phủ 42,65% bình luận OFFENSIVE và 12,36% hai lớp còn lại. Nhóm 20 n-gram thiên về HATE phủ 26,84% HATE và 1,46% hai lớp còn lại. Báo cáo không công khai các chuỗi trích từ bình luận.
- Độ dài HATE cao hơn trong thống kê cũng là một tín hiệu mô tả, nhưng không đủ để tự phân loại.

Các tỷ lệ này không phải Precision, Recall hay độ chính xác của mô hình. Chúng cũng không chứng minh quan hệ nhân quả. Khi xây dựng mô hình sau này, phải chọn đặc trưng trên Train/Validation và chỉ đánh giá Test sau khi đã khóa quy trình.

## Bài thực hành 1 – Baseline F1 Macro

**Kết quả:** Macro F1 lý thuyết `0,301756 ≈ 0,302`; Accuracy lý thuyết là `82,69%`.

**Giải thích:** nếu luôn dự đoán CLEAN, toàn bộ mẫu CLEAN được bắt đúng nhưng không nhận diện được bất kỳ mẫu OFFENSIVE hoặc HATE nào. Accuracy tính theo số mẫu toàn bộ nên bị lớp CLEAN chi phối; Macro F1 cho ba lớp trọng số ngang nhau nên thể hiện rõ hai lớp bị bỏ sót.

## Bài thực hành 3 – Đánh giá bổ sung cho Bài kiểm tra 2

Đề xuất chạy hai kết quả riêng:

1. Giữ nguyên Test chính thức làm kết quả đánh giá chính.
2. Chỉ dùng Train/Validation để chọn tiền xử lý, mô hình và tham số; khóa các lựa chọn đó trước khi xem kết quả Test.
3. Tạo khóa dò văn bản nhất quán bằng chuẩn hóa Unicode NFC, bỏ khoảng trắng đầu/cuối, gộp khoảng trắng liên tiếp và không phân biệt chữ hoa/thường. Nếu dùng bộ chuẩn hóa dự án, áp dụng cùng một quy tắc đã khóa cho cả Train và Test.
4. Tạo thêm một tập nhạy cảm bằng cách bỏ khỏi Test những dòng có khóa văn bản xuất hiện trong Train. Chỉ dùng văn bản để xác định giao nhau; không dùng nhãn Test để chọn hoặc loại dòng.
5. Giữ nguyên lặp và xung đột nhãn nội bộ còn lại trong tập nhạy cảm, đồng thời báo số mẫu, phân bố lớp, lặp và xung đột. Báo cáo kết quả tập này riêng, không thay Test chính thức.
6. Không đổi lựa chọn sau khi xem Test. Không huấn luyện mô hình trong Bài kiểm tra 1.

Theo phép dò đã ghi trong báo cáo, tập nhạy cảm còn **5.866 dòng**: 4.818 CLEAN, 403 OFFENSIVE và 645 HATE; có 5.776 chuỗi duy nhất. Tập này nhỏ hơn và có thể khác phân bố so với Test đầy đủ, nên không đại diện cho toàn bộ Test. Đây là số liệu mô tả thiết kế đánh giá, chưa phải kết quả mô hình.

## Ghi chú học chéo: Bài 2, 4 và 5

Các phần này thuộc phân công chính của Tài; Tú được yêu cầu tự làm để hiểu toàn quy trình.

- **Bài 2 – Trùng Train–Test:** trước xử lý có 792 chuỗi giao, ảnh hưởng 857 dòng Train và 809 dòng Test; sau chuẩn hóa có 797 chuỗi, ảnh hưởng 867 dòng Train và 814 dòng Test. Có 80 chuỗi xung đột nhãn và 96 cặp dòng khác nhãn. “Chuỗi”, “dòng” và “cặp dòng” là ba cách đếm khác nhau.
- **Bài 4 – TF-IDF:** PyVi tách từ cho đặc trưng từ; n-gram từ là (1,2), n-gram ký tự là (2,5). Chỉ Train dùng `fit_transform`; Validation và Test dùng `transform`. Mỗi split có 24.048 / 2.672 / 6.680 hàng; lần lượt có 166.981 chiều từ và 393.272 chiều ký tự, tổng 560.253 chiều. Fit trên Test sẽ làm thông tin của Test ảnh hưởng từ vựng/trọng số.
- **Bài 5 – Chuẩn hóa:** thao tác thử cần chạy trên bản sao, ví dụ `source_copy = frames["train"]["free_text"].copy()`; không ghi đè dữ liệu gốc. Với bộ quy tắc mặc định đã báo cáo, số dòng văn bản thay đổi là 2.921/24.046 ở Train, 336/2.672 ở Validation và 789/6.680 ở Test. Chuẩn hóa có thể làm các câu khác nhau cùng khóa dò; kết quả thay đổi không chứng minh mọi teencode đã được xử lý đúng.

## Mẫu trả lời vấn đáp ngắn

“Nhóm em phân loại bình luận tiếng Việt thành CLEAN, OFFENSIVE và HATE. Dữ liệu có 33.400 mẫu, gồm ba split chính thức. Train mất cân bằng: CLEAN chiếm 82,69%, còn OFFENSIVE chiếm 6,68%, nên nhóm dùng F1 Macro thay vì chỉ nhìn Accuracy. Nếu đoán CLEAN cho mọi mẫu, Accuracy là 82,69% nhưng Macro F1 chỉ khoảng 0,302 và hai lớp nhỏ không được nhận diện. HATE có trung vị độ dài 59 ký tự, cao hơn 31 ký tự ở hai lớp kia, nhưng đây chỉ là thống kê mô tả chứ không phải quy tắc nhãn. Bài kiểm tra 1 chưa huấn luyện mô hình.”

## Trạng thái bằng chứng

- Đây là tài liệu ôn tập, không tự nó chứng minh ai đã thao tác.
- Ngày 2026-10-29, Tú gửi báo cáo chi tiết và tự xác nhận đã chuẩn bị môi trường, tải dữ liệu thật, chạy Notebook, hoàn thành bài 1–5 và trả lời 8 câu vấn đáp. Báo cáo cũng cho biết Tú đã cập nhật checklist và nhật ký cá nhân.
- Codex đối chiếu độc lập các số liệu chính với dữ liệu thật và chạy lại bộ kiểm thử tích hợp: 25 đạt. Việc này xác nhận kết quả kỹ thuật có thể tái lập, không chứng minh độc lập người thực hiện hoặc chất lượng trả lời miệng.
- Nhật ký [`contributions.md`](contributions.md) ghi rõ phần tự xác nhận của Tú, phần được đối chiếu kỹ thuật và giới hạn chứng cứ. Chưa có người quan sát độc lập hoặc xác nhận của giảng viên về vấn đáp/thực hành tại chỗ.
- Tài chưa gửi báo cáo hoàn thành.
