# Nguồn, điều kiện truy cập và cách tái tạo ViHSD

## Nguồn và điều kiện

- Nguồn được dùng: [bộ dữ liệu chính thức `uitnlp/vihsd` trên Hugging Face](https://huggingface.co/datasets/uitnlp/vihsd).
- Tác giả mô tả ViHSD là 33.400 bình luận tiếng Việt gán một trong ba lớp `CLEAN`, `OFFENSIVE`, `HATE`; bài báo gốc là Luu, Nguyen và Nguyen (2021), [arXiv:2103.11528](https://arxiv.org/abs/2103.11528).
- Trang Hugging Face yêu cầu đăng nhập, chấp thuận điều kiện truy cập và chia sẻ thông tin tài khoản Hugging Face. Chủ tài khoản đã chấp thuận và xác thực trong môi trường cục bộ. Không lưu hoặc chia sẻ token.
- Thẻ Hugging Face hiện ghi metadata giấy phép MIT; README của nhóm tác giả ghi dữ liệu chỉ dùng cho mục đích nghiên cứu. Phạm vi hai ghi chú này chưa được làm rõ. Nhóm chỉ dùng dữ liệu trong bài tập/nghiên cứu cục bộ, không đưa bình luận, tệp dữ liệu, hay bản dẫn xuất có thể khôi phục bình luận lên GitHub.

## Schema đã đọc từ dữ liệu thật

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `free_text` | `string` | Nội dung bình luận gốc |
| `label_id` | `int64` | Mã lớp gốc; các mã quan sát được là 0, 1, 2 |

Ánh xạ dùng trong báo cáo là `0 = CLEAN`, `1 = OFFENSIVE`, `2 = HATE`, phù hợp với thứ tự ba lớp trong tài liệu tác giả và cách gắn nhãn của các bản xem mẫu cùng nguồn. Dataset lưu nhãn dưới dạng số nguyên, không khai báo `ClassLabel`; vì vậy mã nguồn giữ nguyên `label_id` và chỉ thêm tên lớp cho bảng phân tích.

| Tập chính thức | Số dòng |
|---|---:|
| Train | 24.048 |
| Validation | 2.672 |
| Test | 6.680 |
| **Tổng** | **33.400** |

Các con số khớp với số lượng và ba split trong bài báo/README tác giả. Lần kiểm tra dữ liệu ghi nhận revision Hugging Face `88e81b36ca376867640dad9df295e0f7d499ab80` (cập nhật kho: 2025-04-06). Hãy ghi revision mới nếu tải lại sau khi nguồn thay đổi.

## Tải, lưu cục bộ và chạy lại

Cài thư viện trong PowerShell:

```powershell
python -m pip install -r requirements.txt
python -m pip install -r requirements-data.txt
```

Đăng nhập Hugging Face bằng `hf auth login` nếu máy chưa có phiên được cấp quyền. Nhập token trực tiếp vào lời nhắc của lệnh; không đưa token vào mã, tệp cấu hình dự án, hay hội thoại.

Tải dữ liệu và lưu định dạng Hugging Face vào vùng cục bộ bị Git bỏ qua:

```python
from datasets import load_dataset

dataset = load_dataset(
    "uitnlp/vihsd",
    revision="88e81b36ca376867640dad9df295e0f7d499ab80",
)
dataset.save_to_disk("data/raw/uitnlp_vihsd")
```

Trong dự án, `python scripts/run_real_dataset_analysis.py` đọc bản cục bộ nếu đã có; nếu chưa có thì truy vấn revision hiện hành, tải đúng `uitnlp/vihsd`, và lưu bản gốc vào `data/raw/uitnlp_vihsd/`. Script kiểm tra split, tên cột, kiểu dữ liệu, số dòng và tập mã nhãn trước khi phân tích. Bảng tổng hợp cục bộ được ghi vào `artifacts/real_vihsd/`; hai biểu đồ không chứa văn bản được ghi vào `reports/figures/`.

Không đổi nhãn, không chia lại ba split chính thức và không ghi đè dữ liệu đầu vào. Dữ liệu gốc và bảng đối chiếu văn bản phải tiếp tục nằm ngoài Git.

## Cách diễn giải nhãn và giới hạn

Các lớp mô tả mức độ nội dung: CLEAN là nội dung không bị gán là xúc phạm/thù ghét; OFFENSIVE là ngôn từ xúc phạm; HATE là ngôn từ thù ghét. Ranh giới này phụ thuộc ngữ cảnh và hướng dẫn gán nhãn; không nên coi các từ đơn lẻ là bằng chứng tuyệt đối của nhãn.

Hai ghi chú giấy phép/điều kiện sử dụng nêu trên chưa được giải quyết về mặt pháp lý. Do đó, không chia sẻ lại bình luận, không đưa ví dụ nguyên văn vào báo cáo công khai, và không đẩy dữ liệu hoặc output notebook có thể chứa văn bản thật lên repository.
