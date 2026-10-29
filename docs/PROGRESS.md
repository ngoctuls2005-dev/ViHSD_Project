# Kế hoạch và nhật ký tiến độ

## Mục tiêu

Hoàn thành trung thực Bài kiểm tra 1 – tuần 4, gồm 10 tiêu chí, trước khi bắt đầu huấn luyện mô hình. Không khẳng định đạt điểm cụ thể; chỉ đánh dấu tiêu chí hoàn tất khi có sản phẩm và bằng chứng kiểm chứng được.

## Trạng thái tổng quan

- Repository: `ngoctuls2005-dev/ViHSD_Project`, nhánh chính `main`.
- Điểm bắt đầu: commit `2f3d61c707359c824921013813f484abcea9ca6c` (`Initial commit`), chỉ có README và `.gitignore`.
- Trạng thái dữ liệu: đã xác thực Hugging Face, tải và xác minh `uitnlp/vihsd` revision `88e81b36ca376867640dad9df295e0f7d499ab80`; bản gốc nằm trong `data/raw/uitnlp_vihsd/` và bị Git bỏ qua. Schema là `free_text:string`, `label_id:int64`; ba split có tổng 33.400 dòng. Metadata license MIT và ghi chú tác giả “chỉ dùng cho nghiên cứu” chưa được đối chiếu; không tái phân phối dữ liệu.
- Trạng thái mô hình: chưa huấn luyện, đúng phạm vi Bài kiểm tra 1.
- Cập nhật gần nhất: 2026-10-29.

## Kế hoạch theo giai đoạn

### Giai đoạn 1 – Khởi tạo dự án và tài liệu bài toán

**Đầu ra:** quy tắc làm việc (`AGENTS.md`), README, phát biểu bài toán, giải thích phương pháp đánh giá, bộ khung báo cáo và kế hoạch theo giai đoạn.

**Điều kiện hoàn thành:** đầu vào/đầu ra và ba lớp được nêu cụ thể; F1 Macro được chọn và giải thích; không ghi kết quả giả; kế hoạch có đầu ra, tiêu chí hoàn thành và ranh giới rõ cho từng giai đoạn.

**Tiêu chí:** 1, 2 và bản hướng dẫn giải thích cho tiêu chí 9. **Trạng thái:** hoàn tất; tài liệu đã được rà soát thủ công. Bằng chứng ban đầu ghi ở nhật ký 2026-10-23.

### Giai đoạn 2 – Khảo sát và phân tích dữ liệu

**Đầu ra:** hướng dẫn tải/tái tạo; xác minh điều kiện sử dụng, schema, kiểu dữ liệu, nhãn và các tập; từ điển dữ liệu; mã EDA; bảng thống kê và biểu đồ có nhận xét dựa trên phép đo; ít nhất ba phân tích quan hệ đặc trưng–nhãn.

**Điều kiện hoàn thành:** số mẫu/cột/kiểu dữ liệu và phân bố nhãn được tạo từ dữ liệu thật; nguồn và giới hạn sử dụng được ghi rõ; biểu đồ có tiêu đề, nhãn trục và nhận xét cụ thể; không công khai bình luận thật trái điều kiện.

**Tiêu chí:** 3, 4, 5. **Trạng thái:** hoàn tất trên dữ liệu thật. Đã ghi schema, số lượng, phân bố nhãn/độ dài, biểu đồ và ba nhận xét có số liệu trong báo cáo. Lệnh tái tạo là `python scripts/run_real_dataset_analysis.py`.

### Giai đoạn 3 – Phát hiện và xử lý chất lượng dữ liệu

**Đầu ra:** module phân tích vấn đề dữ liệu; module tiền xử lý có thể tái sử dụng; bảng trước/sau; unit test cho quy tắc chuẩn hóa.

**Điều kiện hoàn thành:** định lượng thiếu/rỗng, trùng, trùng khác nhãn, nhãn không hợp lệ, bất thường, teencode, ký tự lặp, mất cân bằng và rò rỉ; xử lý có kiểm soát, giữ phủ định/dấu câu/emoji có ý nghĩa, không sửa nhãn và không ghi đè bản gốc; có ví dụ an toàn.

**Tiêu chí:** 6, 7. **Trạng thái:** hoàn tất thống kê và so sánh trước/sau trên dữ liệu thật. Hai dòng văn bản thiếu ở Train, trùng lặp trong/giữa split, xung đột nhãn và ngoại lệ đã được định lượng. Chuẩn hóa chỉ tạo bản dẫn xuất; không sửa nhãn hoặc xóa dòng.

### Giai đoạn 4 – Chuẩn bị dữ liệu và đặc trưng

**Đầu ra:** mã giữ tập chính thức hoặc chia phân tầng có seed; tách từ tiếng Việt; TF-IDF n-gram từ và ký tự; kiểm tra số mẫu, số chiều, nhãn và tính không rò rỉ.

**Điều kiện hoàn thành:** vectorizer chỉ `fit` trên Train, chỉ `transform` Validation/Test; không oversampling hay học thống kê trên toàn bộ dữ liệu; không dùng Test để chọn tham số/đặc trưng; có kiểm thử phù hợp.

**Tiêu chí:** 8. **Trạng thái:** đã kiểm chứng trên ba split thật. PyVi và TF-IDF từ/ký tự tạo 560.253 chiều; chỉ Train được fit, Validation/Test chỉ transform. Đã phát hiện 792 chuỗi chuẩn hóa trùng Train–Test trước tiền xử lý (797 sau), cần giữ cảnh báo này cho mọi đánh giá mô hình.

### Giai đoạn 5 – Báo cáo, kiểm thử và chuẩn bị vấn đáp

**Đầu ra:** báo cáo `reports/exam1_report.md` hoàn chỉnh cho tiêu chí 1–9; notebook thực hành; câu hỏi và trả lời gợi ý; hướng dẫn chạy trên Windows; bằng chứng kiểm thử và bảng đóng góp/nhật ký.

**Điều kiện hoàn thành:** notebook chạy lại từ đầu trên dữ liệu có quyền sử dụng; bảng, hình và số liệu được tạo từ kết quả thực tế; mọi giới hạn/chưa xác minh được nêu; sinh viên có thể giải thích và thao tác lại.

**Tiêu chí:** 9, 10 và hoàn thiện minh chứng cho 1–8. **Trạng thái:** báo cáo, notebook dữ liệu thật, câu hỏi vấn đáp và kiểm thử đã cập nhật. Notebook đã chạy hết code cell trên dữ liệu thật; sinh viên vẫn cần tự thực hành và giải thích kết quả cá nhân.

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
- Commit `e6a57e2` (`docs: khoi tao ke hoach va tai lieu ViHSD`) đã tạo trên `main`; lần push thất bại vì máy không phân giải được `github.com`.
- Commit `9158cef` (`feat: them cong cu EDA va xac minh nguon ViHSD`) đã tạo trên `main`; lần push ban đầu thất bại do DNS, sau đó đã được đẩy cùng các giai đoạn còn lại.

### 2026-10-23 – Công cụ EDA có thể tái sử dụng

- Thêm hướng dẫn nguồn/truy cập, bộ đọc CSV không giả định tên cột, kiểm tra schema theo tên cột người chạy chỉ định, thống kê nhãn/độ dài/n-gram bề mặt/dấu hiệu viết và vẽ biểu đồ tổng hợp.
- Thêm lệnh `scripts/run_eda.py`; đầu ra cục bộ vào `artifacts/eda/`, không ghi nội dung bình luận vào bảng độ dài hoặc bảng dấu hiệu.
- Kiểm tra đóng gói: `python -m pip install -e . --no-deps` thành công; trợ giúp CLI chạy được.
- Kiểm thử: `python -m unittest discover -s tests -v` — 8 kiểm thử đạt trên fixture nhỏ dùng cho kiểm thử kỹ thuật; không phải kết quả ViHSD.
- Hạn chế: chưa có schema/cột/thống kê thực tế. Giai đoạn 2 và tiêu chí 3–5 vẫn chưa hoàn thành cho tới khi có quyền truy cập dữ liệu.

### 2026-10-23 – Phát hiện lỗi và tiền xử lý bảo toàn văn bản

- Thêm bảng thống kê thiếu/rỗng, kiểu dữ liệu văn bản, trùng sau NFC/chuẩn hóa khoảng trắng/không phân biệt hoa thường, trùng khác nhãn, nhãn ngoài danh sách, ký tự điều khiển/lặp, teencode và ngoại lệ độ dài theo IQR.
- Thêm thống kê cân bằng lớp và kiểm tra số văn bản trùng giữa các split; đầu ra không chứa nội dung bình luận.
- Thêm module tiền xử lý dùng Unicode NFC, gộp khoảng trắng và từ điển viết tắt có kiểm soát; giữ phủ định, dấu câu, emoji và bản gốc. Bảng đối chiếu văn bản được cảnh báo chỉ dùng cục bộ.
- Kiểm thử: `python -m unittest discover -s tests -v` — 15 kiểm thử đạt trên fixture kỹ thuật; không phải kết quả ViHSD.
- Hạn chế: chưa thể định lượng vấn đề, chọn quy tắc theo tần suất thật hoặc so sánh trước/sau trên ViHSD. Tiêu chí 6–7 vẫn chưa hoàn tất.
- Commit `878fbef` (`feat: them kiem tra chat luong va tien xu ly van ban`) đã tạo trên `main` và hiện đã được đẩy lên GitHub.

### 2026-10-23 – Chia hold-out và chuẩn bị TF-IDF

- Thêm cách giữ nguyên split chính thức có kiểm tra schema; phương án dự phòng chia ba tập có phân tầng và `random_state` cố định.
- Thêm kiểm tra dừng khi có bình luận trùng giữa các split theo quy tắc NFC/khoảng trắng/không phân biệt hoa thường.
- Thêm adapter tách từ tiếng Việt bằng PyVi và hai TF-IDF riêng: n-gram từ, n-gram ký tự. `fit_transform` chỉ chạy trên Train; Validation/Test chỉ `transform`; nhãn được giữ theo đúng thứ tự.
- Kiểm thử: `python -m unittest discover -s tests -v` — 21 kiểm thử đạt trên fixture kỹ thuật. Kiểm thử TF-IDF dùng tokenizer giả lập để không phụ thuộc package PyVi; PyVi chưa được cài trong môi trường hiện tại.
- Chưa có dữ liệu thật để xác nhận split nào là chính thức, kích thước ma trận, lỗi trùng lặp thực tế hay tính phù hợp của từ vựng. Tiêu chí 8 vẫn chưa hoàn tất.
- Commit `43f2bd5` (`feat: chuan bi split va dac trung TF-IDF`) đã tạo trên `main` và hiện đã được đẩy lên GitHub.

### 2026-10-23 – Notebook thực hành và vấn đáp

- Thêm `notebooks/exam1_practice.ipynb` với chế độ fixture được cảnh báo rõ, chế độ CSV yêu cầu điền cột đã xác minh, đếm nhãn, vẽ biểu đồ, thống kê độ dài, rà soát trùng, thử quy tắc chuẩn hóa và so sánh trước/sau.
- Thêm câu hỏi/trả lời gợi ý cho hold-out, chia tập, F1 Macro, mất cân bằng, rò rỉ và giới hạn của fixture.
- Notebook được chạy từ đầu trong kiểm thử bằng fixture và không lưu output vào tệp; kiểm thử toàn bộ: `python -m unittest discover -s tests -v` — 22 kiểm thử đạt.
- Chưa chạy notebook với dữ liệu thật; sinh viên vẫn cần tự thực hành và giải thích số liệu. Báo cáo cuối vẫn chờ dữ liệu thật cho các tiêu chí 3–8.

## Trạng thái bàn giao – 2026-10-23

- Năm commit giai đoạn đã được đẩy thành công lên `origin/main`, đến commit `287ffbc` (`docs: them notebook thuc hanh va huong dan van dap`). Lần push đầu gặp lỗi phân giải DNS; push sau đã thành công.
- Trước khi push, kiểm tra diff và danh sách tệp xác nhận không có `TEC/`, dữ liệu ViHSD, `.env` hay bình luận thật. Notebook được commit không có output.
- Kiểm thử cuối: `python -m unittest discover -s tests -v` — 22 kiểm thử đạt; `python -m compileall -q src scripts tests` đạt; kiểm tra liên kết/tệp Markdown và notebook sạch đạt.
- Tiêu chí 1–2 và tài liệu hướng dẫn tiêu chí 9 đã được viết; tiêu chí 10 có notebook và câu hỏi luyện tập. Tiêu chí 3–8 chưa thể công bố hoàn tất vì chưa truy cập được nội dung ViHSD, nên chưa có schema, thống kê, biểu đồ, bảng vấn đề hay kích thước ma trận từ dữ liệu thật.

## Bằng chứng và giới hạn còn lại

- Trang [ViHSD trên Hugging Face](https://huggingface.co/datasets/uitnlp/vihsd) ghi ba lớp và metadata license MIT; README [repository của nhóm tác giả](https://github.com/sonlam1102/vihsd) ghi 33.400 bình luận và “chỉ dùng cho nghiên cứu”. Phạm vi hai ghi chú sử dụng chưa được làm rõ; không tái phân phối dữ liệu.
- Schema, số dòng, nhãn, phân bố, độ dài, chất lượng, chuẩn hóa và kích thước TF-IDF đã được kiểm chứng trực tiếp trên revision ghi trong báo cáo. Bảng tổng hợp không chứa bình luận.
- Dữ liệu gốc chỉ tồn tại cục bộ trong `data/raw/`; `TEC/` tiếp tục nằm ngoài Git.
- Còn 792 chuỗi chuẩn hóa trùng Train–Test trước xử lý và 797 sau; cần nêu rủi ro này khi thực hiện Bài kiểm tra 2. Chưa huấn luyện mô hình và chưa có kết quả dự đoán.
- Sinh viên cần tự chạy notebook, giải thích lựa chọn và hoàn thành thao tác tại chỗ; sản phẩm này không thay thế phần thực hành cá nhân.

### 2026-10-29 – Phân tích ViHSD thật và hoàn tất minh chứng cho tiêu chí 3–8

- Đọc lại `AGENTS.md`, `docs/PROGRESS.md`, `TEC/Task.md` và `TEC/Evaluation_Criteria.md`; kiểm tra Git ban đầu sạch ở `main` trên commit `054c5c0fadc9661b6391b948778415eb9dbab1e2`.
- `hf auth whoami` xác nhận phiên Hugging Face đã đăng nhập. `load_dataset("uitnlp/vihsd")` chạy thành công; repository revision `88e81b36ca376867640dad9df295e0f7d499ab80`. Split/schema: Train 24.048, Validation 2.672, Test 6.680; `free_text:string`, `label_id:int64`; tổng 33.400 dòng; mã quan sát được `{0,1,2}` và ánh xạ dùng là 0=CLEAN, 1=OFFENSIVE, 2=HATE.
- Lưu bản gốc bằng `DatasetDict.save_to_disk` tại `data/raw/uitnlp_vihsd/`; `git check-ignore` xác nhận `/data/raw/` bị bỏ qua. Không ghi bình luận thật vào bảng tổng hợp, notebook hay Git.
- Thêm `scripts/run_real_dataset_analysis.py`; chạy `python scripts/run_real_dataset_analysis.py` thành công. Script ghi bảng tổng hợp vào `artifacts/real_vihsd/` (bị bỏ qua) và hai biểu đồ không chứa văn bản vào `reports/figures/`.
- EDA: Train có 19.886 CLEAN (82,69%), 1.606 OFFENSIVE (6,68%), 2.556 HATE (10,63%); tỷ lệ lớp đông/lớp ít 12,38. Trung vị độ dài ký tự: CLEAN 31, OFFENSIVE 31, HATE 59. Phân tích từ/cụm từ dùng Train; nhóm 20 n-gram thiên về OFFENSIVE phủ 42,65% OFFENSIVE và 12,36% các lớp còn lại; nhóm thiên về HATE phủ 26,84% HATE và 1,46% lớp khác.
- Kiểm tra chất lượng: Train có 2 văn bản thiếu, 1.535 dòng trùng dư trong split, 292 dòng thuộc nhóm trùng khác nhãn và 1.837 ngoại lệ độ dài theo 1,5×IQR; nhãn sai/thiếu, kiểu văn bản sai và ký tự điều khiển đều bằng 0. Có 792 chuỗi chuẩn hóa trùng Train–Test trước tiền xử lý và 797 sau; không xóa hoặc chia lại vì cần giữ split chính thức và ghi nhận nguy cơ đánh giá lạc quan.
- Tiền xử lý: Unicode NFC, khoảng trắng và từ điển viết tắt hữu hạn; so sánh trước/sau trong bản dẫn xuất, giữ nhãn/số dòng và dữ liệu gốc. Văn bản thay đổi: Train 2.921/24.046 (12,15%), Validation 336/2.672 (12,57%), Test 789/6.680 (11,81%). Chuẩn hóa làm số giao nhau Train–Test tăng từ 792 lên 797 nên rủi ro được giữ nguyên trong báo cáo.
- Cài PyVi `0.1.1`; TF-IDF từ n-gram (1,2) và ký tự (2,5): 166.981 + 393.272 = 560.253 chiều. Fit chỉ trên Train; Validation/Test chỉ transform. Không huấn luyện mô hình.
- Cập nhật báo cáo `reports/exam1_report.md`, hướng dẫn nguồn, README, notebook và câu hỏi vấn đáp. Notebook mặc định dùng ViHSD thật và không lưu output; đã chạy tuần tự toàn bộ 6 code cell với ba split thật, sinh ma trận 560.253 chiều.
- Bổ sung kiểm thử tích hợp tùy chọn với Hugging Face và notebook thật. Lệnh `$env:VIHSD_RUN_INTEGRATION='1'; python -m unittest discover -s tests -v` chạy **24 kiểm thử đạt**; `python -m compileall -q src scripts tests` đạt. Unit test notebook dùng fixture chỉ để kiểm thử kỹ thuật, còn kiểm thử tích hợp xác minh dữ liệu thật.
- Trạng thái tiêu chí: 3–8 có bằng chứng trên ViHSD thật; 1–2 có tài liệu; 9 có hướng dẫn tự giải thích; 10 có notebook/bài tập nhưng sinh viên vẫn cần thực hành cá nhân. Không tự khẳng định điểm.
- Điều kiện sử dụng chưa được làm rõ: metadata Hugging Face ghi MIT, README tác giả ghi “chỉ dùng cho nghiên cứu”. Không đẩy dữ liệu gốc, bình luận, token hoặc đầu ra có văn bản.
- Trạng thái Git/commit/push sẽ được ghi sau bước rà soát cuối cùng ở lượt này.
