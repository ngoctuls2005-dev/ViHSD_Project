# Nguồn và cách truy cập ViHSD

## Nguồn được kiểm tra

- [Thẻ bộ dữ liệu `uitnlp/vihsd`](https://huggingface.co/datasets/uitnlp/vihsd) mô tả ViHSD là dữ liệu phân loại văn bản tiếng Việt, khoảng 33 nghìn bình luận, ba nhãn `HATE`, `OFFENSIVE`, `CLEAN`, định dạng CSV và các split `train`, `validation`, `test`.
- Trang Hugging Face hiển thị metadata license `MIT`, đồng thời yêu cầu người dùng đăng nhập/chấp thuận điều kiện và chia sẻ thông tin tài khoản để truy cập nội dung.
- [README của nhóm tác giả](https://github.com/sonlam1102/vihsd) ghi 33.400 bình luận, hướng dẫn liên hệ tác giả để lấy dữ liệu và nêu dữ liệu chỉ dùng cho nghiên cứu.

## Trích dẫn bài báo

Luu, Son T.; Nguyen, Kiet Van; Nguyen, Ngan Luu-Thuy. (2021). “A Large-scale Dataset for Hate Speech Detection on Vietnamese Social Media Texts.” *IEA/AIE 2021*, tr. 415–426. [arXiv:2103.11528](https://arxiv.org/abs/2103.11528), [DOI nhà xuất bản](https://doi.org/10.1007/978-3-030-79457-6_35).

Hai ghi chú về quyền sử dụng có thể áp dụng cho các phần khác nhau của kho hoặc dataset. Nhóm chưa xác minh được phạm vi áp dụng, nên không tải bằng tài khoản của người khác, không đăng lại dữ liệu và không công khai bình luận. Nếu cần chia sẻ dữ liệu hoặc đưa bình luận vào đầu ra, cần đọc điều kiện được chấp thuận và xin xác nhận từ chủ sở hữu dữ liệu.

## Khả năng tái tạo khi đã được cấp quyền

Thẻ Hugging Face hướng dẫn dùng thư viện `datasets` với các split dưới đây. Đây là hướng dẫn để người dùng có quyền thực hiện; lệnh chưa chạy trong môi trường dự án vì phiên này chưa chấp thuận điều kiện truy cập.

```python
from datasets import load_dataset

train = load_dataset("sonlam1102/vihsd", split="train")
validation = load_dataset("sonlam1102/vihsd", split="validation")
test = load_dataset("sonlam1102/vihsd", split="test")
```

Sau khi có quyền truy cập:

1. Ghi lại revision/phiên bản bộ dữ liệu mà thư viện báo về.
2. Kiểm tra các trường và kiểu dữ liệu trực tiếp; không mặc định tên cột hoặc kiểu mã hóa nhãn.
3. Lưu dữ liệu chỉ trong thư mục `data/raw/` cục bộ, bị Git bỏ qua.
4. Đối chiếu số dòng giữa từng split và nguồn; ghi checksum nếu xuất file CSV.
5. Truyền tên cột đã xác minh cho `scripts/run_eda.py`.
6. Không đưa file dữ liệu hay ví dụ bình luận thật vào repository công khai.

Cài thêm thư viện tải dataset nếu cần: `python -m pip install -r requirements-data.txt`.

## Trạng thái hiện tại

Chưa chấp thuận điều kiện Hugging Face và chưa đọc được nội dung dữ liệu trong phiên này. Vì vậy chưa xác minh được schema thực tế, số mẫu theo split/lớp, mã hóa nhãn, checksum hoặc quyền tái phân phối. Các bộ dữ liệu nhỏ trong unit test chỉ dùng để kiểm tra kỹ thuật; chúng không phải ViHSD và không tạo kết quả nghiên cứu.
