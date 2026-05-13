# Flow Free Solver

Ứng dụng desktop viết bằng `Tkinter` để tạo và giải puzzle kiểu **Flow Free** bằng 2 hướng tiếp cận:

- `DFS Backtracking`
- `SAT Solver` với `Z3`

Người dùng có thể tự tạo board, chọn puzzle mẫu, lưu/tải puzzle từ file và so sánh hiệu năng hai solver bằng script benchmark đi kèm.

## Tính năng chính

- Tạo board kích thước `n x n` khi khởi động ứng dụng
- Đặt endpoint bằng cách nhập nhãn màu rồi click lên lưới
- Giải puzzle bằng `Solve` (DFS) hoặc `Solve SAT` (Z3)
- `Reset Path` để xóa lời giải nhưng giữ endpoint
- `Clear Board` để làm trống toàn bộ board
- `Load Puzzle` để nạp puzzle mẫu từ [puzzles.py](puzzles.py)
- `Save File` và `Load File` để lưu/tải puzzle dạng text
- Chạy benchmark qua [benchmark.py](benchmark.py)

## Yêu cầu

- Python `3.10+`
- `tkinter` đi kèm Python
- Dependency trong [requirements.txt](requirements.txt)

## Cài đặt

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Nếu bạn không dùng virtual environment thì chỉ cần:

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
python main.py
```

Khi mở app, chương trình sẽ hỏi kích thước board `n`. Sau khi xác nhận, giao diện chính sẽ hiển thị để bạn nhập endpoint và chạy solver.

## Cách sử dụng

1. Nhập tên màu hoặc nhãn màu vào ô `Màu`, ví dụ `red`, `blue`, `green`, `A`, `pipe1`.
2. Click lên 2 ô để đặt 2 endpoint cho cùng một màu.
3. Nhấn `Solve` để giải bằng DFS hoặc `Solve SAT` để giải bằng Z3.
4. Dùng `Reset Path` nếu muốn bỏ lời giải hiện tại nhưng giữ nguyên endpoint.
5. Dùng `Clear Board` nếu muốn tạo lại puzzle từ đầu.
6. Dùng `Load Puzzle` để nạp puzzle mẫu có sẵn.
7. Dùng `Save File` hoặc `Load File` để lưu/tải puzzle từ file `.txt`.

## Lưu ý về dữ liệu đầu vào

- Mỗi màu phải có đúng `2 endpoint` trước khi giải.
- Nếu một màu đã có đủ 2 endpoint, app sẽ chặn không cho đặt thêm.
- Nếu nhãn là tên màu hợp lệ của `Tkinter` như `red`, `orange`, `cyan`, giao diện sẽ dùng đúng màu đó.
- Nếu nhãn không phải tên màu chuẩn, app vẫn hỗ trợ và sẽ tự sinh màu hiển thị.

## Chạy benchmark

```bash
python benchmark.py
```

Script này chạy cả hai solver trên các puzzle mẫu trong [puzzles.py](puzzles.py) và in ra:

- kết quả giải được hay không
- thời gian chạy của DFS
- thời gian chạy của SAT
- solver nào nhanh hơn trên từng puzzle

## Định dạng file puzzle

Puzzle được lưu dưới dạng text, mỗi dòng là một hàng của lưới, các ô cách nhau bằng dấu phẩy:

```text
red,.,.,.,blue
.,.,green,.,.
.,.,.,.,.
.,.,.,.,.
blue,.,green,.,red
```

Quy ước:

- `.` là ô trống
- mọi giá trị khác `.` được xem là endpoint

## Thuật toán

### DFS Backtracking

Solver trong [solve.py](solve.py) dùng:

- sắp xếp màu theo khoảng cách Manhattan giữa 2 endpoint
- ưu tiên mở rộng các bước đi gần đích hơn
- kiểm tra ràng buộc bậc để cắt nhánh sớm

Ý tưởng chính là nối từng cặp màu theo thứ tự hợp lý, quay lui khi gặp trạng thái không còn khả năng tạo lời giải hợp lệ.

### SAT Solver

Solver trong [sat_solver.py](sat_solver.py) mã hóa bài toán thành các ràng buộc SAT với `Z3`, gồm:

- biến màu cho từng ô
- biến cạnh cho từng bước nối giữa hai ô kề nhau
- biến `rank` để đảm bảo đường đi có thứ tự và tránh chu trình

Hướng này thường ổn định hơn trên các puzzle trung bình hoặc khó, nhưng chi phí dựng ràng buộc cũng cao hơn.

## Cấu trúc dự án

| File | Vai trò |
|------|---------|
| [main.py](main.py) | Khởi tạo app, hỏi kích thước board rồi mở GUI |
| [gui.py](gui.py) | Giao diện Tkinter, thao tác với lưới, load/save puzzle, gọi solver |
| [board.py](board.py) | Quản lý trạng thái grid, endpoint và metadata của board |
| [solve.py](solve.py) | Solver DFS backtracking |
| [sat_solver.py](sat_solver.py) | Solver SAT dùng Z3 |
| [puzzles.py](puzzles.py) | Puzzle mẫu và hàm đọc/ghi file puzzle |
| [benchmark.py](benchmark.py) | Script benchmark hai solver |

## Hướng phát triển thêm

- thêm kiểm tra tính hợp lệ của file puzzle khi import
- thêm nhiều puzzle mẫu hơn
- hiển thị thời gian solve trực tiếp trên GUI
- bổ sung test tự động cho parser và solver
