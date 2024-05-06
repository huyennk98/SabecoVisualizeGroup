# Hướng Dẫn Chạy Chương Trình

- Bước 1: Đăng ký tài khoản trên Github, và gửi Github username cũng như yêu cầu truy cập vào repo dự án đến email [chaunguyen1993vn@gmail.com]() <br>
    Format của email như sau: <br>
    (Tiêu Đề) Gửi yêu cầu view Github repo & làm việc cùng đến anh Châu <br>
    (Nội Dung Email) <br>
    Github Username: abcxyz <br>
    Dự Án Muốn View: vrp_dashboard_visualization (Nhánh first_essential_dashboard)

- Bước 2: Đăng nhập vào tài khoản email liên kết với tài khoản Github, và xác nhận sẽ là cộng tác viên (collaborator) của dự án

- Bước 3: Sau khi trở thành cộng tác viên (collaborator) của repo dự án, clone dự án về máy local theo 1 trong 2 cách sau:
  - a. Nếu dùng command line interface / Git Bash / Linux Terminal: Di chuyển tới thư mục để code dự án, sau đó clone dự án với dòng lệnh:
    ```git
      git clone https://github.com/chaunguyen1993ece/vrp_dashboard_visualization.git
    ```
  - b. Nếu dùng Github Desktop: Nhấn chuột vào thanh File -> Clone repository -> Copy & paste URL của dự án (ô màu đỏ) & chọn đường dẫn vào thư mục dự án (ô màu xanh lá):
    ![Clone Project](../images/clone_prj.png)

- Bước 4:
  - a. Nếu dùng command line interface / Git Bash / Linux Terminal:
    - Di chuyển vào trong thư mục dự án & chuyển nhánh:
    ```git
      cd vrp_dashboard_visualization
      git checkout first_essential_dashboard
    ```
    - Khởi tạo virtual environment (venv) và cài đặt các thư viện:
    ```git
      python3 -m virtualenv venv
    ```
    - Kích hoạt virtual environment (venv)
        - Với Linux:
        ```git
        source venv/bin/activate
        ```
        - Với Windows:
        ```git
        venv\Scripts\activate
        ```
    - Cài đặt các thư viện bằng lệnh sau:
    ```git
      pip install -r requirements.txt
    ```
    - Chạy chương trình:
    ```git
      python dashboard_app.py
    ```
    - Nhấn vào đường link http://127.0.0.1:8050/
    - Từ đó, Dashboard sẽ hiện ra trên trình duyệt
  - b. Nếu dùng IDE (PyCharm):
    - Nhấn chuột vào thanh Current repository, chọn vrp_dashboard_visualization (ô màu cam)
    - Sau đó, rê chuột qua thanh Current branch (ô màu đỏ) & click chuột chọn nhánh first_essential_branch (ô màu xanh dương):
    ![Switch Branch](../images/switch_branch.png)
    - Dùng IDE để cài đặt các thư viện (trong file requirements.txt) tự động
    - Tìm file dashboard_app.py trong thư mục gốc chương trình (ô màu đỏ)
    - Nhấn nút chạy chương trình (ô màu xanh lá, nút xanh lá)
    - Nhấn vào đường link http://127.0.0.1:8050/ (ô màu vàng)
    - Từ đó, Dashboard sẽ hiện ra trên trình duyệt
    ![Run App](../images/run_app.png)
