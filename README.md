# PTHTTM - Assignment 2

Dự án này là bài tập lớn số 2 của môn học Phát triển Hệ thống Thông minh (PTHTTM). Dự án bao gồm việc phân tích dữ liệu, huấn luyện mô hình học máy, xây dựng REST API và các ứng dụng cho ba bài toán khác nhau.

## Cấu trúc thư mục

Dự án được chia thành các thư mục chính như sau:

- `customer_behavior/`: Bài toán phân tích hành vi khách hàng dựa trên đánh giá sản phẩm thương mại điện tử (Womens Clothing E-Commerce Reviews). Bao gồm EDA, huấn luyện mô hình, REST API.
- `diabetes/`: Bài toán dự đoán bệnh tiểu đường. Bao gồm file Jupyter notebook phân tích, thiết lập Neo4j (`setup_neo4j.py`), và REST API.
- `house_price/`: Bài toán dự đoán giá nhà. Bao gồm notebook phân tích dữ liệu, mô hình dự đoán và REST API.
- `report/`: Chứa mã nguồn LaTeX và báo cáo chi tiết cho toàn bộ dự án.

## Thành phần trong mỗi bài toán

Trong mỗi thư mục bài toán (ví dụ: `diabetes`, `house_price`, `customer_behavior`), bạn sẽ tìm thấy:
- **Jupyter Notebooks (`.ipynb`)**: Chứa mã nguồn phân tích dữ liệu khám phá (EDA) và huấn luyện mô hình.
- **`REST_API.py`**: Mã nguồn khởi tạo server Flask/FastAPI (hoặc web framework khác) để cung cấp API phục vụ dự đoán/truy vấn.
- **`requirements.txt`**: Danh sách các thư viện Python cần thiết để chạy dự án.
- **Thư mục `model/` (hoặc `models/`)**: Nơi lưu trữ các file mô hình đã được huấn luyện.
- **Thư mục `mobile/`**: Source code ứng dụng di động cho hệ thống.
- **Thư mục `templates/`**: Chứa các file HTML nếu API có cung cấp giao diện web.

## Hướng dẫn cài đặt

1. Mở terminal và clone (hoặc mở) thư mục dự án này.
2. Với mỗi bài toán bạn muốn chạy, hãy di chuyển vào thư mục tương ứng. Ví dụ:
   ```bash
   cd diabetes
   ```
3. Khuyến nghị tạo một môi trường ảo (virtual environment) trước khi cài đặt:
   ```bash
   python -m venv venv
   source venv/bin/activate  # (Trên Windows dùng: venv\Scripts\activate)
   ```
4. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
5. Chạy API:
   ```bash
   python REST_API.py
   ```

## Báo cáo

Toàn bộ tài liệu báo cáo của dự án nằm trong thư mục `report/`. Để biên dịch file báo cáo, bạn cần có môi trường LaTeX trên máy.
