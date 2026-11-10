# Tài – Bắt đầu Bài kiểm tra 2

## Việc cần học và tự làm

1. Đọc `docs/exam2_plan.md`, phần Pipeline và chống rò rỉ trong `docs/exam2_research.md`.
2. Mở `src/vihsd/models.py`, `src/vihsd/model_evaluation.py` và `src/vihsd/experiment.py`; lần theo dữ liệu từ văn bản đến vectorizer, classifier và metrics.
3. Tự chạy thử đầy đủ:

```powershell
python -m pytest -q tests
python scripts/run_exam2_experiments.py --features word --cv-folds 3
```

4. Mở `reports/exam2_results/cv_folds.csv`, `cv_summary.csv`, `selection.json` và `test_metrics.csv`. Xác nhận CV fit vectorizer trong từng fold, model được chốt bằng Validation trước Test.
5. Tự thay cấu hình `C` hoặc `class_weight` trên Validation/fixture để quan sát thay đổi. Không chạy lặp Test để chọn cấu hình.

## Vì sao cần làm

Tiêu chí 3–5 yêu cầu Pipeline, chạy được, đánh giá CV đúng. ViHSD có văn bản trùng nên cần phân biệt stratified và grouped CV. Tiêu chí cá nhân 8–10 yêu cầu Tài giải thích và thao tác trực tiếp; mã do Codex tạo không xác nhận thay phần đó.

## Minh chứng cần ghi

Ghi ngày tự chạy, lệnh, cấu hình đã thay, file kết quả đọc, ý nghĩa của trung bình/độ lệch chuẩn theo fold và việc Test được giữ khỏi lựa chọn. Không đưa nội dung bình luận hay token vào nhật ký.
