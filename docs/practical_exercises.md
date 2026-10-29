# Năm bài thực hành cá nhân – Bài kiểm tra 1

Các con số bên dưới đã được xác minh trên ViHSD thật revision `88e81b36ca376867640dad9df295e0f7d499ab80`. Bài tập là việc mỗi sinh viên tự làm và giải thích; các kết quả đã có trong báo cáo không tự xác nhận rằng một người đã thực hành. Không huấn luyện mô hình ở các bài này.

## Bài 1 – Tính baseline F1 Macro

- **Phụ trách chính:** Hoàng Ngọc Tú. **Tự học chéo:** Lê Quang Tài.
- **Trạng thái cá nhân:** Tú tự báo cáo đã hoàn thành ngày 2026-10-29; phép tính đã được đối chiếu. Tài chưa xác nhận.
- **Mục đích:** Hiểu ảnh hưởng của mất cân bằng lớp và phân biệt mức tham chiếu lý thuyết với kết quả mô hình.
- **Yêu cầu:** Tự tính Macro F1 nếu luôn dự đoán CLEAN, chỉ dùng phân bố Train.
- **Các bước:**
  1. Mở phần 4 của [`reports/exam1_report.md`](../reports/exam1_report.md) hoặc bảng phân bố trong notebook.
  2. Tính Precision CLEAN = `19.886 / 24.048 = 0,8269`; Recall CLEAN = `1`.
  3. Tính F1 CLEAN = `2 × Precision × Recall / (Precision + Recall) = 0,9053`.
  4. F1 của OFFENSIVE và HATE bằng `0`; lấy trung bình cộng ba F1.
- **Kết quả đã xác minh:** Macro F1 lý thuyết `0,3018 ≈ 0,302`. Accuracy của chiến lược hằng này là 82,69%, nhưng hai lớp nhỏ không được nhận diện.
- **Giải thích dễ hiểu:** Mốc 0,302 được tính từ số nhãn Train; chưa có mô hình nào được huấn luyện hoặc dự đoán.
- **Câu hỏi tự kiểm tra:** Vì sao F1 của OFFENSIVE và HATE bằng 0? Vì sao chỉ nói Accuracy 82,69% dễ gây hiểu nhầm?
- **Điều kiện xác nhận:** Sinh viên tự trình bày phép tính và giải thích được khác biệt giữa Accuracy và Macro F1; ghi bằng chứng vào nhật ký.
- [ ] Tôi đã tự làm và giải thích; trạng thái chỉ được người học xác nhận trong [`docs/contributions.md`](contributions.md).

## Bài 2 – Kiểm toán trùng Train–Test

- **Phụ trách chính:** Lê Quang Tài. **Tự học chéo:** Hoàng Ngọc Tú.
- **Trạng thái cá nhân:** Tú tự báo cáo đã hoàn thành phần học chéo ngày 2026-10-29; số liệu đã được đối chiếu. Tài chưa xác nhận.
- **Mục đích:** Hiểu vì sao cùng một văn bản ở Train và Test có thể làm đánh giá lạc quan, và vì sao khác nhãn cũng cần được báo cáo.
- **Yêu cầu:** Tạo lại bảng tổng hợp giao nhau trước/sau chuẩn hóa; không mở hay xuất văn bản bình luận.
- **Tệp cần mở:** `scripts/run_real_dataset_analysis.py`; kết quả tổng hợp cục bộ `artifacts/real_vihsd/train_test_duplicate_audit.csv`; phần 6 trong báo cáo.
- **Các bước:**
  1. Từ thư mục gốc dự án, chạy `python scripts/run_real_dataset_analysis.py`.
  2. Đọc bảng audit tổng hợp. Có thể lọc an toàn các cột bằng PowerShell:

     ```powershell
     Import-Csv .\artifacts\real_vihsd\train_test_duplicate_audit.csv |
       Select-Object stage, shared_unique_texts, split_a_rows_affected, split_b_rows_affected, conflicting_unique_texts, differing_label_row_pairs
     ```

  3. So sánh số chuỗi, dòng bị ảnh hưởng và cặp dòng khác nhãn. Không đưa các tệp khác trong `artifacts/real_vihsd/` lên GitHub; một số bảng cục bộ chứa n-gram rút ra từ văn bản.
- **Kết quả đã xác minh:** Trước xử lý: 792 chuỗi giao, 857 dòng Train và 809 dòng Test bị ảnh hưởng. Sau xử lý: 797 chuỗi, 867 dòng Train và 814 dòng Test. Cả hai lần có 80 chuỗi xung đột nhãn và 96 cặp dòng khác nhãn.
- **Giải thích dễ hiểu:** Một chuỗi có thể xuất hiện ở nhiều dòng, nên số chuỗi duy nhất, số dòng bị ảnh hưởng và số cặp dòng khác nhãn không phải cùng một đại lượng. Xung đột nhãn được thống kê, không tự sửa.
- **Câu hỏi tự kiểm tra:** Vì sao 80 chuỗi xung đột không bằng 96 cặp dòng? Vì sao không xóa hoặc sửa nhãn tự động?
- **Điều kiện xác nhận:** Tự chạy lệnh, đọc được các số liệu chính, phân biệt ba kiểu đếm và giải thích được rủi ro mà không tiết lộ văn bản.
- [ ] Tôi đã tự làm và giải thích; trạng thái chỉ được người học xác nhận trong [`docs/contributions.md`](contributions.md).

## Bài 3 – Đề xuất đánh giá bổ sung cho Bài kiểm tra 2

- **Phụ trách chính:** Hoàng Ngọc Tú. **Tự học chéo:** Lê Quang Tài.
- **Trạng thái cá nhân:** Tú tự báo cáo đã hoàn thành ngày 2026-10-29; thiết kế và số liệu đã được đối chiếu. Tài chưa xác nhận.
- **Mục đích:** Đề xuất cách đo ảnh hưởng của nội dung lặp mà vẫn giữ kết quả trên Test chính thức.
- **Yêu cầu:** Trình bày quy trình bổ sung, chưa chạy mô hình.
- **Tệp cần mở:** Mục “Phương án đánh giá bổ sung cho Bài kiểm tra 2” trong phần 6 của [`reports/exam1_report.md`](../reports/exam1_report.md), cùng `docs/evaluation_guide.md`.
- **Các bước:**
  1. Nêu cách tạo khóa dò từ văn bản NFC, khoảng trắng chuẩn hóa và không phân biệt hoa/thường.
  2. Giữ Train/Validation/Test chính thức. Dùng Train/Validation để chọn quy trình; khóa tiền xử lý và siêu tham số trước khi đọc kết quả Test.
  3. Ngoài kết quả Test chính thức, đề xuất một phép nhạy cảm chỉ loại các dòng Test có khóa văn bản xuất hiện trong Train.
  4. Giữ các lặp/xung đột nội bộ của tập nhạy cảm và báo riêng; không dùng nhãn Test để chọn hoặc loại dòng.
- **Kết quả đã xác minh:** Sau lọc trùng chéo bằng văn bản còn 5.866 dòng Test và 5.776 chuỗi duy nhất. Đây là thống kê mô tả thiết kế, chưa phải kết quả mô hình.
- **Giải thích dễ hiểu:** Kết quả bổ sung giúp nhìn riêng các dòng không thấy trong Train nhưng không thay Test chính thức. Không xem kết quả Test rồi đổi lựa chọn mô hình.
- **Câu hỏi tự kiểm tra:** Vì sao phải khóa pipeline trước khi đánh giá? Vì sao tập nhạy cảm không đại diện toàn bộ Test?
- **Điều kiện xác nhận:** Tự mô tả được thứ tự lựa chọn/đánh giá và khẳng định rõ không huấn luyện hoặc chọn mô hình dựa trên Test trong bài này.
- [ ] Tôi đã tự làm và giải thích; trạng thái chỉ được người học xác nhận trong [`docs/contributions.md`](contributions.md).

## Bài 4 – PyVi và TF-IDF

- **Phụ trách chính:** Lê Quang Tài. **Tự học chéo:** Hoàng Ngọc Tú.
- **Trạng thái cá nhân:** Tú tự báo cáo đã hoàn thành phần học chéo ngày 2026-10-29; cách fit/transform và số chiều đã được đối chiếu. Tài chưa xác nhận.
- **Mục đích:** Xác định nơi văn bản được tách từ, nơi TF-IDF được fit và kích thước biểu diễn.
- **Yêu cầu:** Giải thích mã và đọc bảng kích thước, không huấn luyện bộ phân loại.
- **Tệp cần mở:** `src/vihsd/preparation.py`, cell cuối “5. Chuẩn bị TF-IDF” của `notebooks/exam1_practice.ipynb`, và `artifacts/real_vihsd/tfidf_dimensions.csv` sau khi chạy script.
- **Các bước:**
  1. Tìm `fit_transform` và `transform` trong `src/vihsd/preparation.py` (Ctrl+F trong VS Code).
  2. Chạy notebook từ trên xuống trên dữ liệu thật, hoặc chạy script phân tích như ở Bài 2.
  3. Đọc số hàng, số chiều từ và ký tự, tổng chiều; không in từ vựng/chuỗi đặc trưng.
- **Kết quả đã xác minh:** Train 24.048 hàng, Validation 2.672, Test 6.680. TF-IDF từ có 166.981 chiều; TF-IDF ký tự có 393.272; tổng là 560.253 chiều ở mỗi split.
- **Giải thích dễ hiểu:** Train dùng `fit_transform` để học từ vựng và trọng số. Validation/Test chỉ `transform` bằng những gì Train đã học; không tạo bộ từ vựng mới từ hai tập này.
- **Câu hỏi tự kiểm tra:** Vì sao không fit riêng trên Test? PyVi làm gì trước khi tạo n-gram từ?
- **Điều kiện xác nhận:** Chỉ đúng dòng lệnh fit/transform, nêu đủ ba kích thước và giải thích được vì sao giữ thứ tự nhãn.
- [ ] Tôi đã tự làm và giải thích; trạng thái chỉ được người học xác nhận trong [`docs/contributions.md`](contributions.md).

## Bài 5 – Thử quy tắc chuẩn hóa trên bản sao

- **Phụ trách chính:** Lê Quang Tài. **Tự học chéo:** Hoàng Ngọc Tú.
- **Trạng thái cá nhân:** Tú tự báo cáo đã hoàn thành phần học chéo ngày 2026-10-29; số liệu tổng hợp đã được đối chiếu. Tài chưa xác nhận.
- **Mục đích:** Đo tác động của một quy tắc mà không ghi đè văn bản nguồn.
- **Yêu cầu:** Dùng một bản sao Series, tính tóm tắt trước/sau và giải thích giới hạn.
- **Tệp cần mở:** `src/vihsd/preprocessing.py`, cell “4. Chuẩn hóa có kiểm soát” trong notebook và `docs/preprocessing.md`.
- **Các bước:**
  1. Chạy notebook từ đầu để tạo `frames`.
  2. Trong một cell tạm mới, sao chép cột văn bản Train rồi áp dụng một quy tắc rõ ràng:

     ```python
     source_copy = frames["train"]["free_text"].copy()
     trial_copy = normalize_series(source_copy, {"ko": "không"})
     print(preprocessing_summary(source_copy, trial_copy))
     ```

  3. Ghi số dòng, số dòng thay đổi và số ký tự trước/sau. Không in văn bản trước/sau, không sửa `data/raw/` hoặc từ điển mặc định.
- **Kết quả đã xác minh:** Với bộ quy tắc mặc định, Train có 2.921/24.046 dòng văn bản không thiếu thay đổi (12,15%); Validation 336/2.672 (12,57%); Test 789/6.680 (11,81%). Dò giao Train–Test tăng từ 792 lên 797 chuỗi sau chuẩn hóa. Quy tắc thử riêng `{"ko": "không"}` có số thay đổi khác và không cần khớp các số này.
- **Giải thích dễ hiểu:** Chuẩn hóa làm một số dạng viết thành cùng hình thức, nhưng cũng có thể nhập hai câu khác nhau vào cùng khóa. Thay đổi số liệu không chứng minh mọi cách viết đã được xử lý đúng.
- **Câu hỏi tự kiểm tra:** Vì sao dùng `.copy()`? Vì sao giữ phủ định, dấu câu và nhãn? Điều gì có thể gây tăng số chuỗi giao nhau?
- **Điều kiện xác nhận:** Tự chạy trên bản sao, chỉ báo cáo số tổng hợp và giải thích rủi ro; dữ liệu gốc còn nguyên.
- [ ] Tôi đã tự làm và giải thích; trạng thái chỉ được người học xác nhận trong [`docs/contributions.md`](contributions.md).

## Ghi nhận sau khi tự làm

Tú đã gửi báo cáo tự xác nhận ngày 2026-10-29; các mục chi tiết được ghi trong [`docs/contributions.md`](contributions.md). Tài vẫn cần tự ghi ngày, bài đã làm, kết quả mình giải thích được, bằng chứng và xác nhận của chính mình. Các ô “Tôi đã tự làm” dưới từng bài vẫn là checklist cá nhân cho người đọc; không tick thay cho thành viên khác. Việc đối chiếu số liệu không phải là quan sát độc lập phần thực hành hoặc vấn đáp.

