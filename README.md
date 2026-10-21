# Lab 9 – Kiểm thử tự động với Selenium

Bài thực hành xây dựng các test case kiểm thử tự động bằng **Selenium WebDriver (Python)** và **pytest** cho website demo [The Internet](https://the-internet.herokuapp.com/).



## 1. Mục tiêu

- Làm quen với Selenium WebDriver thông qua tài liệu và video hướng dẫn.
- Viết tối thiểu 05 test case tự động cho một website bất kỳ (bài này thực hiện 8 test case, 9 lần chạy do có data-driven).
- Áp dụng các kỹ thuật cơ bản: locator, thao tác phần tử, xử lý alert, dropdown, explicit wait, kiểm thử theo dữ liệu (parametrize).

## 2. Công nghệ sử dụng

| Thành phần | Phiên bản |
|---|---|
| Python | 3.14.7 |
| Selenium | 4.x (tự quản lý chromedriver qua Selenium Manager) |
| pytest | 9.1.1 |
| pytest-html | 4.2.0 |
| Trình duyệt | Google Chrome |
| Hệ điều hành | Windows 11 |

## 3. Cấu trúc thư mục

```
lab9/
├── test_the_internet.py   # Mã nguồn các test case
├── README.md              # Tài liệu này
└── report.html            # Báo cáo kết quả (tạo sau khi chạy với --html)
```

## 4. Cài đặt

1. Cài [Python 3](https://www.python.org/downloads/) và Google Chrome.
2. Cài các thư viện cần thiết:

```bash
pip install selenium pytest pytest-html
```

> Selenium 4.6 trở lên tự tải chromedriver phù hợp với Chrome trên máy, không cần cấu hình thủ công. Máy cần có kết nối Internet.

## 5. Cách chạy

Chạy toàn bộ test:

```bash
pytest test_the_internet.py -v
```

Chạy một test cụ thể:

```bash
pytest test_the_internet.py -v -k "tc01"
```

Xuất báo cáo HTML:

```bash
pytest test_the_internet.py -v --html=report.html --self-contained-html
```

Chạy ẩn trình duyệt (headless):

```powershell
# PowerShell
$env:HEADLESS=1; pytest test_the_internet.py -v

# CMD
set HEADLESS=1 && pytest test_the_internet.py -v

# Linux / macOS
HEADLESS=1 pytest test_the_internet.py -v
```

## 6. Danh sách test case

Dữ liệu đăng nhập hợp lệ của trang demo: `tomsmith` / `SuperSecretPassword!`

| ID | Chức năng | Các bước thực hiện | Kết quả mong đợi |
|---|---|---|---|
| TC01 | Đăng nhập thành công | 1. Mở `/login`<br>2. Nhập username, password hợp lệ<br>3. Nhấn Login | Chuyển đến `/secure`, hiện thông báo "You logged into a secure area!" |
| TC02 | Đăng nhập thất bại (2 bộ dữ liệu) | 1. Mở `/login`<br>2. Nhập sai password **hoặc** sai username<br>3. Nhấn Login | Ở lại `/login`, hiện "Your password is invalid!" hoặc "Your username is invalid!" |
| TC03 | Đăng xuất | 1. Đăng nhập thành công<br>2. Nhấn Logout | Quay về `/login`, hiện "You logged out of the secure area!" |
| TC04 | Checkbox | 1. Mở `/checkboxes`<br>2. Kiểm tra trạng thái mặc định<br>3. Click cả hai checkbox | Checkbox 1 chuyển sang tick, checkbox 2 chuyển sang bỏ tick |
| TC05 | Dropdown | 1. Mở `/dropdown`<br>2. Chọn "Option 2", sau đó chọn "Option 1" | Giá trị được chọn hiển thị đúng sau mỗi lần chọn |
| TC06 | Thêm / xoá phần tử | 1. Mở `/add_remove_elements/`<br>2. Nhấn Add Element 3 lần<br>3. Nhấn Delete 1 lần | Sau bước 2 có 3 nút Delete, sau bước 3 còn 2 nút |
| TC07 | JavaScript Alerts | 1. Mở `/javascript_alerts`<br>2. Alert → OK<br>3. Confirm → Cancel<br>4. Prompt → nhập "Selenium" → OK | Kết quả lần lượt: "You successfully clicked an alert", "You clicked: Cancel", "You entered: Selenium" |
| TC08 | Dynamic Loading (Explicit Wait) | 1. Mở `/dynamic_loading/1`<br>2. Nhấn Start<br>3. Chờ nội dung xuất hiện | Hiển thị "Hello World!" sau khi tải xong |

## 7. Kỹ thuật Selenium được sử dụng

- **Locator:** `By.ID`, `By.CSS_SELECTOR`, `By.XPATH`, `By.CLASS_NAME`
- **Thao tác:** `click()`, `send_keys()`, `is_selected()`, `is_displayed()`
- **Dropdown:** lớp `Select` (`select_by_visible_text`, `select_by_value`)
- **Alert:** `switch_to.alert` (`accept`, `dismiss`, `send_keys`)
- **Đồng bộ:** `implicitly_wait` và `WebDriverWait` + `expected_conditions`
- **pytest:** `fixture` (khởi tạo / đóng trình duyệt), `parametrize` (kiểm thử theo dữ liệu), `assert`

## 8. Kết quả chạy

```
platform win32 -- Python 3.14.7, pytest-9.1.1
collected 9 items

test_tc01_login_success ........................... PASSED
test_tc02_login_fail[wrong_password] .............. PASSED
test_tc02_login_fail[wrong_username] .............. PASSED
test_tc03_logout .................................. PASSED
test_tc04_checkboxes .............................. PASSED
test_tc05_dropdown ................................ PASSED
test_tc06_add_remove_elements ..................... PASSED
test_tc07_javascript_alerts ....................... PASSED
test_tc08_dynamic_loading_explicit_wait ........... PASSED

9 passed in 84.89s (0:01:24)
```

**Tổng kết:** 9/9 test PASSED (tỷ lệ 100%).

1.png

## 9. Xử lý sự cố thường gặp

| Lỗi | Cách khắc phục |
|---|---|
| `SessionNotCreatedException` (lệch phiên bản driver) | Cập nhật Selenium: `pip install -U selenium` và cập nhật Chrome |
| Selenium không tải được driver | Kiểm tra kết nối Internet / proxy |
| `NoSuchElementException` | Trang tải chậm hoặc đổi giao diện, dùng `WebDriverWait` thay vì chờ cố định |
| Test chạy chậm | Dùng chế độ headless (`HEADLESS=1`) |

## 10. Tài liệu tham khảo

- Tài liệu chính thức Selenium: <https://www.selenium.dev/documentation/>
- Website thực hành: <https://the-internet.herokuapp.com/>
- Tài liệu pytest: <https://docs.pytest.org/>
