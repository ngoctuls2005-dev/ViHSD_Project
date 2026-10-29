# Bắt đầu tại đây – Lê Quang Tài

Tài đã gửi báo cáo tự xác nhận hoàn thành 10 bước ngày **2026-10-29**. Các số liệu kỹ thuật chính được đối chiếu với dữ liệu thật và bảng tổng hợp; phần tự thao tác/vấn đáp không được ghi nhận như quan sát độc lập. Các dấu kiểm dưới đây phản ánh báo cáo của Tài. Không chia sẻ token, dữ liệu gốc, bình luận thật hoặc thư mục artifact lên GitHub; Bài kiểm tra 1 không yêu cầu huấn luyện mô hình.

## 1. Tải dự án từ GitHub và mở trong VS Code

- **Mục đích:** Lấy mã nguồn và tài liệu hiện hành của nhóm.
- **Tệp cần mở:** Sau khi tải, mở `README.md`; hướng dẫn riêng này nằm trong `docs/START_HERE_TAI.md`.
- **Các bước:** Mở PowerShell tại thư mục muốn lưu dự án, chạy các lệnh dưới. Sau đó mở thư mục mới trong VS Code. Nếu VS Code không nhận lệnh `code`, chọn **File → Open Folder…** và tự chọn thư mục `ViHSD_Project`.
- **Lệnh:**

  ```powershell
  git clone https://github.com/ngoctuls2005-dev/ViHSD_Project.git
  cd ViHSD_Project
  code .
  ```

- **Kết quả mong đợi:** Trong VS Code thấy `README.md`, `src`, `docs`, `notebooks`, `scripts` và `reports`.
- **Giải thích:** Repository Public chứa mã và tài liệu; dữ liệu gốc không có trong Git và phải được tải hợp lệ riêng.
- **Lỗi thường gặp:** Nếu `git` hoặc `code` không nhận diện, cài Git/VS Code hoặc mở dự án bằng nút giao diện **Open Folder**. Nếu thư mục đã được clone, không clone lồng thêm; kiểm tra `git status` và hỏi nhóm trước khi cập nhật nếu có thay đổi riêng.
- **Bằng chứng cần lưu:** Ghi ngày và commit đang dùng; commit một mình không chứng minh đã thực hành cá nhân.
- [x] Tự hoàn thành và ghi vào nhật ký (Tài tự báo cáo).

## 2. Tạo và chọn môi trường Python

- **Mục đích:** Cài thư viện vào môi trường riêng của dự án để Notebook dùng đúng phiên bản.
- **Tệp cần mở:** `pyproject.toml`, `requirements.txt`, `requirements-data.txt`.
- **Các bước:** Trong terminal PowerShell của VS Code, xác nhận đang ở gốc dự án (`Test-Path .\README.md` phải là `True`); tạo môi trường; cài thư viện; chọn `.venv` làm interpreter và Jupyter kernel trong VS Code (`Ctrl+Shift+P` → **Python: Select Interpreter**).
- **Lệnh:**

  ```powershell
  py -3 --version
  py -3 -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  python -m pip install -e .
  python -m pip install -r requirements-data.txt
  ```

- **Kết quả mong đợi:** Python 3.10 trở lên và thư viện pandas, scikit-learn, PyVi, matplotlib, datasets dùng được trong `.venv`.
- **Giải thích:** `requirements-data.txt` cài thêm thư viện truy cập Hugging Face; `.venv` giúp tách thư viện dự án khỏi Python khác trên máy.
- **Lỗi thường gặp:** Nếu kích hoạt PowerShell bị chặn, không đổi chính sách lâu dài; chọn `.venv\Scripts\python.exe` làm interpreter hoặc chạy `\.venv\Scripts\python.exe -m pip ...`. Nếu Notebook báo thiếu module, kiểm tra kernel có phải `.venv` không.
- **Bằng chứng cần lưu:** Ghi phiên bản Python và xác nhận kernel `.venv`, không chụp thông tin tài khoản.
- [x] Tự hoàn thành và ghi vào nhật ký (Tài tự báo cáo).

## 3. Đăng nhập Hugging Face bằng tài khoản được cấp quyền

- **Mục đích:** Lấy ViHSD từ nguồn chính thức theo quyền của chính Tài.
- **Tệp cần mở:** Trang [`uitnlp/vihsd`](https://huggingface.co/datasets/uitnlp/vihsd) và `docs/data_access.md`.
- **Các bước:** Đăng nhập Hugging Face bằng tài khoản của Tài trên trang dataset; đọc và chấp thuận điều kiện truy cập nếu tài khoản được yêu cầu. Trong PowerShell, xác thực CLI bằng token riêng tại lời nhắc. Nếu chưa được cấp quyền, dùng yêu cầu truy cập của Hugging Face và chờ được chấp thuận; không dùng tài khoản/token của Tú.
- **Lệnh:**

  ```powershell
  hf auth login
  hf auth whoami
  ```

- **Kết quả mong đợi:** `hf auth whoami` xác nhận phiên đăng nhập của Tài. Token không xuất hiện trong lệnh, tài liệu, ảnh chụp hay Git.
- **Giải thích:** Việc clone repository công khai không tự cấp quyền dữ liệu có kiểm soát. Notebook chỉ tải được dataset sau khi tài khoản được phép.
- **Lỗi thường gặp:** Lỗi 401/403: kiểm tra đúng tài khoản, đã chấp thuận điều kiện và quyền đã được cấp. `hf` không nhận diện: cài lại `requirements-data.txt`, mở terminal mới rồi thử lại. Không gửi token cho nhóm/Codex để nhờ đăng nhập.
- **Bằng chứng cần lưu:** Chỉ ghi “đã xác thực/đã yêu cầu quyền/đang chờ”; không lưu token, ảnh trang cá nhân hay thông tin nhạy cảm.
- [x] Tự hoàn thành và ghi trạng thái đúng vào nhật ký (Tài tự báo cáo).

## 4. Mở Notebook và nạp ViHSD thật

- **Mục đích:** Chạy quy trình nhóm đã có trên ba split chính thức.
- **Tệp cần mở:** `notebooks/exam1_practice.ipynb`.
- **Các bước:** Mở notebook trong VS Code, chọn kernel `.venv`, đặt chế độ fixture về `0` trong terminal, rồi chạy code cell đầu tiên. Cell này dùng dữ liệu ở `data/raw/uitnlp_vihsd/` nếu đã có; nếu chưa, nó tải dữ liệu khi tài khoản có quyền. Chạy sáu code cell từ trên xuống bằng **Run All**.
- **Lệnh:**

  ```powershell
  $env:VIHSD_NOTEBOOK_USE_FIXTURE = "0"
  Test-Path .\data\raw\uitnlp_vihsd
  ```

- **Kết quả mong đợi:** Train 24.048, Validation 2.672, Test 6.680; tổng 33.400. Cột `free_text` là chuỗi, `label_id` là số nguyên; mã nhãn 0=CLEAN, 1=OFFENSIVE, 2=HATE.
- **Giải thích:** Notebook không chia lại dữ liệu. Fixture là dữ liệu giả chỉ để thử mã và không được dùng làm kết quả báo cáo.
- **Lỗi thường gặp:** Nếu hiện `FIXTURE MINH HOA`, đặt biến về `0`, khởi động lại kernel và chạy từ đầu. Nếu thiếu dữ liệu, hoàn thành bước 3 rồi chạy lại. Nếu không thấy module, quay lại bước 2 và chọn đúng kernel.
- **Bằng chứng cần lưu:** Ghi ba kích thước split và revision ghi trong báo cáo; không lưu/đẩy Notebook có output. Sau khi xem, dùng **Clear All Outputs** trước khi lưu hoặc chia sẻ.
- [x] Tự hoàn thành và ghi vào nhật ký (Tài tự báo cáo; số liệu kỹ thuật đã đối chiếu).

## 5. Đọc kết quả trong báo cáo mục 6–8

- **Mục đích:** Hiểu chất lượng dữ liệu, lý do chuẩn hóa và cách tạo đặc trưng.
- **Tệp cần mở:** Các mục 6, 7, 8 của `reports/exam1_report.md`; đối chiếu `docs/preprocessing.md` và `docs/vectorization.md`.
- **Các bước:** Đọc bảng vấn đề; phân biệt chuỗi trùng, số dòng bị ảnh hưởng, cặp dòng khác nhãn; đọc bảng thay đổi trước/sau; cuối cùng đọc bảng số chiều TF-IDF.
- **Lệnh:** Không cần lệnh riêng; chạy Notebook trước nếu muốn xác nhận lại tại chỗ.
- **Kết quả mong đợi:** Nêu được 792/797 chuỗi giao Train–Test, 809/814 dòng Test bị ảnh hưởng, 80 chuỗi xung đột và 96 cặp khác nhãn; TF-IDF tổng 560.253 chiều.
- **Giải thích:** Chuẩn hóa tạo văn bản dẫn xuất, không sửa văn bản/nhãn gốc. Nhãn Test chỉ được dùng trong báo cáo để audit, không chọn quy tắc hay mô hình.
- **Lỗi thường gặp:** Không gọi 792 chuỗi là 792 dòng; không kết luận chuẩn hóa luôn tốt chỉ vì số token viết tắt phát hiện giảm; không xem n-gram như quan hệ nhân quả.
- **Bằng chứng cần lưu:** Viết tóm tắt 3–5 câu bằng lời của mình, không chép bình luận ví dụ.
- [x] Tự hoàn thành và ghi vào nhật ký (Tài tự báo cáo; kết quả đã đối chiếu).

## 6. Tái tạo kiểm toán trùng lặp

- **Mục đích:** Kiểm tra giao Train–Test và hiểu xung đột nhãn mà không xuất nội dung.
- **Tệp cần mở:** `scripts/run_real_dataset_analysis.py`; bảng tổng hợp `artifacts/real_vihsd/train_test_duplicate_audit.csv`; Bài 2 trong `docs/practical_exercises.md`.
- **Các bước:** Từ thư mục gốc chạy script; sau đó chỉ chọn các cột thống kê tổng hợp như dưới đây. Không mở/chia sẻ `text_signals_by_label.csv` hoặc toàn bộ thư mục artifacts.
- **Lệnh:**

  ```powershell
  python scripts/run_real_dataset_analysis.py
  Import-Csv .\artifacts\real_vihsd\train_test_duplicate_audit.csv |
    Select-Object stage, shared_unique_texts, split_a_rows_affected, split_b_rows_affected, conflicting_unique_texts, differing_label_row_pairs
  ```

- **Kết quả mong đợi:** Trước: 792 chuỗi, 857 dòng Train, 809 dòng Test, 80 chuỗi xung đột, 96 cặp khác nhãn. Sau: 797, 867, 814, 80, 96. Theo nhãn, dòng giao Train CLEAN 759→769, OFFENSIVE 42→42, HATE 56→56; Test CLEAN 725→730, OFFENSIVE 41→41, HATE 43→43.
- **Giải thích:** Tăng số giao nhau đến từ 5 chuỗi và thêm các dòng CLEAN; số xung đột không tăng. Không sửa nhãn và không chia lại split.
- **Lỗi thường gặp:** Nếu file CSV chưa có, kiểm tra script kết thúc thành công và dữ liệu được cấp quyền. Nếu truy cập Hugging Face lỗi, quay lại bước 3. Không đưa output `artifacts/` lên Git.
- **Bằng chứng cần lưu:** Ghi các số tổng hợp và lời giải thích; không lưu nội dung bình luận.
- [x] Tự hoàn thành và ghi vào nhật ký (Tài tự báo cáo; kết quả audit đã đối chiếu).

## 7. Thử chuẩn hóa trên bản sao dữ liệu

- **Mục đích:** Thấy quy tắc tác động đến bao nhiêu dòng mà không sửa nguồn.
- **Tệp cần mở:** `src/vihsd/preprocessing.py`; code cell **4. Chuẩn hóa có kiểm soát** trong Notebook; Bài 5 trong `docs/practical_exercises.md`.
- **Các bước:** Chạy notebook từ đầu để có biến `frames`. Thêm cell tạm mới, sao chép văn bản Train, áp dụng một quy tắc thử và chỉ in tóm tắt số liệu:

  ```python
  source_copy = frames["train"]["free_text"].copy()
  trial_copy = normalize_series(source_copy, {"ko": "không"})
  print(preprocessing_summary(source_copy, trial_copy))
  ```

- **Lệnh:** Chạy cell tạm trong Notebook; không ghi cell thử vào notebook công khai cùng output.
- **Kết quả mong đợi:** Có `row_count`, `non_missing_row_count`, `changed_row_count`, tỷ lệ đổi và tổng ký tự trước/sau. Với quy tắc mặc định của báo cáo, Train có 2.921/24.046 dòng không thiếu thay đổi; quy tắc thử riêng ở trên có thể cho số khác.
- **Giải thích:** `.copy()` tạo đầu vào thử riêng. Quy tắc viết tắt có thể đổi cách biểu diễn và làm chuỗi khác nhau nhập thành cùng khóa.
- **Lỗi thường gặp:** `NameError` thường do chưa chạy cell nạp/chuẩn hóa hoặc kernel vừa khởi động lại; chạy lại notebook từ đầu. Không sửa `data/raw/`, không đổi nhãn, không in `source_copy`/`trial_copy`.
- **Bằng chứng cần lưu:** Chỉ ghi bảng số tổng hợp và nêu quy tắc đã thử; bỏ văn bản bình luận khỏi ảnh chụp.
- [x] Tự hoàn thành và ghi vào nhật ký (Tài tự báo cáo; thống kê đã đối chiếu).

## 8. Tìm `fit_transform`, `transform` và kích thước TF-IDF

- **Mục đích:** Kiểm tra rò rỉ và hiểu kích thước biểu diễn trước mô hình.
- **Tệp cần mở:** `src/vihsd/preparation.py`; code cell cuối **5. Chuẩn bị TF-IDF**; `artifacts/real_vihsd/tfidf_dimensions.csv`.
- **Các bước:** Trong VS Code nhấn `Ctrl+F`, tìm `fit_transform`, rồi tìm `.transform(`. Đọc bảng kích thước được in ở cuối notebook hoặc trong báo cáo, không in vocabulary.
- **Lệnh:** Chạy Notebook/script như bước 4/6; không cần huấn luyện classifier.
- **Kết quả mong đợi:** Train 24.048 hàng; Validation 2.672; Test 6.680. N-gram từ 166.981 chiều, ký tự 393.272, tổng 560.253 chiều mỗi split.
- **Giải thích:** Hai vectorizer được fit trên Train; Validation/Test chỉ transform bằng vocabulary và IDF đã học. Đây là tạo đặc trưng, chưa phải huấn luyện mô hình phân loại.
- **Lỗi thường gặp:** Nếu ma trận có kích thước khác, xác nhận đã nạp đúng revision/split và chạy cell từ đầu. Không fit riêng lại trên Validation/Test.
- **Bằng chứng cần lưu:** Ghi vị trí fit/transform trong mã và ba số chiều; không chụp danh sách từ vựng.
- [x] Tự hoàn thành và ghi vào nhật ký (Tài tự báo cáo; mã và số liệu đã đối chiếu).

## 9. Tự làm phần thực hành của Tú

- **Mục đích:** Tài hiểu được bài toán, baseline và cách đánh giá bổ sung của cả nhóm.
- **Tệp cần mở:** Bài 1 và 3 trong `docs/practical_exercises.md`; mục 2 và mục 6 trong `reports/exam1_report.md`.
- **Các bước:** Tự tính baseline `0,3018 ≈ 0,302`; sau đó nói lại phương án giữ Test chính thức và làm phép nhạy cảm lọc chỉ bằng khóa văn bản.
- **Lệnh:** Không cần lệnh riêng; có thể dùng máy tính để kiểm tra phép tính.
- **Kết quả mong đợi:** Phân biệt rõ baseline từ phân bố Train với kết quả mô hình; biết quy trình bổ sung chỉ là đề xuất cho Bài kiểm tra 2.
- **Giải thích:** Không dùng nhãn Test hoặc kết quả Test để chọn quy tắc/model; Bài kiểm tra 1 chưa huấn luyện model.
- **Lỗi thường gặp:** Gọi 0,302 là điểm mô hình; dùng tập Test con thay hẳn Test chính thức; thay đổi quy trình sau khi xem Test.
- **Bằng chứng cần lưu:** Tự viết phép tính và 3–5 câu giải thích trong nhật ký.
- [x] Tự hoàn thành và ghi vào nhật ký (Tài tự báo cáo).

## 10. Ghi kết quả và báo đã hoàn thành

- **Mục đích:** Để nhóm biết chính xác phần Tài đã tự thực hiện.
- **Tệp cần mở:** Mục **Lê Quang Tài** trong `docs/contributions.md`.
- **Các bước:** Tài đã gửi báo cáo chi tiết; nhật ký [`docs/contributions.md`](contributions.md) được đồng bộ theo báo cáo ngày 2026-10-29. Nếu có chi tiết chưa chính xác, Tài cần tự sửa phần của mình.
- **Lệnh:** Không cần lệnh. Nếu muốn lấy SHA đang dùng, chạy `git rev-parse HEAD`.
- **Kết quả mong đợi:** Nhật ký thể hiện sự tự thực hành của Tài; trạng thái chỉ đổi sau khi Tài xác nhận.
- **Giải thích:** Tệp nhóm và commit do Codex chuẩn bị là tài liệu hỗ trợ, không phải minh chứng thao tác cá nhân.
- **Lỗi thường gặp:** Không điền ngày/kết quả khi chưa làm; không đánh dấu bài của Tú; không đưa mã sinh viên, token hoặc bình luận vào bản công khai.
- **Bằng chứng cần lưu:** Ghi phần Tài tự xác nhận; nếu có ảnh, chỉ dùng bảng số tổng hợp.
- [x] Tôi đã tự cập nhật nhật ký và thông báo cho nhóm (Tài tự báo cáo).
