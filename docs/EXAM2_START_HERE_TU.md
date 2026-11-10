# Tú – Bắt đầu Bài kiểm tra 2

## Việc cần học và tự làm

1. Đọc `docs/exam2_research.md`, phần Dummy, Naive Bayes, Logistic Regression và Linear SVC.
2. Mở `src/vihsd/models.py`; giải thích `NumpyMultinomialNB.fit`, smoothing `alpha`, prior lớp và lý do giữ TF-IDF sparse.
3. Tự chạy kiểm thử đối chiếu NB:

```powershell
python -m pytest -q tests/test_models_and_evaluation.py
```

4. Tự mở `notebooks/exam2_practice.ipynb`, chạy các cell từ đầu bằng dữ liệu được cấp quyền. So sánh baseline với ít nhất NB và Linear SVC trên Validation.
5. Mở `reports/exam2_results/validation_model_metrics.csv` và confusion matrix; tự giải thích ít nhất một lỗi CLEAN/OFFENSIVE/HATE mà không sao chép bình luận gốc.

## Vì sao cần làm

Tiêu chí 1–2 yêu cầu nêu lý do thuật toán và có baseline thật. Tiêu chí 6–7 yêu cầu đọc metrics theo lớp, confusion matrix và phân tích lỗi. Tiêu chí cá nhân 8–10 cần Tú tự trả lời và thao tác; kết quả Codex không thay thế phần này.

## Minh chứng cần ghi

Ghi ngày tự làm, lệnh, model/hàm đã sửa hoặc chạy, chỉ số đã đọc, giải thích bằng lời của Tú và câu hỏi còn chưa rõ. Không ghi “hoàn thành” nếu mới đọc tài liệu hoặc chạy thay bởi người khác.
