"""
Bộ test tự động bằng Selenium (Python + pytest)
Website: https://the-internet.herokuapp.com/

Cài đặt:
    pip install selenium pytest pytest-html

Chạy:
    pytest test_the_internet.py -v
    pytest test_the_internet.py -v --html=report.html --self-contained-html
    HEADLESS=1 pytest test_the_internet.py -v        (chạy ẩn trình duyệt)
"""
import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

BASE_URL = "https://the-internet.herokuapp.com"
USERNAME = "tomsmith"
PASSWORD = "SuperSecretPassword!"


# ---------------------------------------------------------------- Fixtures
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,768")
    drv = webdriver.Chrome(options=options)  # Selenium 4.6+ tự tải chromedriver
    drv.implicitly_wait(3)
    yield drv
    drv.quit()


# ----------------------------------------------------------------- Helpers
def login(driver, username, password):
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


def flash_text(driver):
    return driver.find_element(By.ID, "flash").text


# --------------------------------------------------------------- Test cases
def test_tc01_login_success(driver):
    """TC01: Đăng nhập thành công với tài khoản hợp lệ."""
    login(driver, USERNAME, PASSWORD)

    assert "/secure" in driver.current_url
    assert "You logged into a secure area!" in flash_text(driver)
    assert driver.find_element(By.CSS_SELECTOR, "a.button.secondary").is_displayed()


@pytest.mark.parametrize(
    "username, password, expected",
    [
        (USERNAME, "sai_mat_khau", "Your password is invalid!"),
        ("sai_user", PASSWORD, "Your username is invalid!"),
    ],
    ids=["wrong_password", "wrong_username"],
)
def test_tc02_login_fail(driver, username, password, expected):
    """TC02: Đăng nhập thất bại (sai mật khẩu / sai username) - data-driven."""
    login(driver, username, password)

    assert "/login" in driver.current_url
    assert expected in flash_text(driver)


def test_tc03_logout(driver):
    """TC03: Đăng xuất sau khi đăng nhập thành công."""
    login(driver, USERNAME, PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "a.button.secondary").click()

    assert "/login" in driver.current_url
    assert "You logged out of the secure area!" in flash_text(driver)


def test_tc04_checkboxes(driver):
    """TC04: Tick / bỏ tick checkbox."""
    driver.get(f"{BASE_URL}/checkboxes")
    boxes = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input")

    # Trạng thái mặc định: checkbox 1 chưa tick, checkbox 2 đã tick
    assert not boxes[0].is_selected()
    assert boxes[1].is_selected()

    boxes[0].click()
    boxes[1].click()

    assert boxes[0].is_selected()
    assert not boxes[1].is_selected()


def test_tc05_dropdown(driver):
    """TC05: Chọn giá trị trong dropdown."""
    driver.get(f"{BASE_URL}/dropdown")
    select = Select(driver.find_element(By.ID, "dropdown"))

    select.select_by_visible_text("Option 2")
    assert select.first_selected_option.text == "Option 2"

    select.select_by_value("1")
    assert select.first_selected_option.text == "Option 1"


def test_tc06_add_remove_elements(driver):
    """TC06: Thêm 3 phần tử, xoá 1 phần tử -> còn 2."""
    driver.get(f"{BASE_URL}/add_remove_elements/")
    add_btn = driver.find_element(By.XPATH, "//button[text()='Add Element']")

    for _ in range(3):
        add_btn.click()
    assert len(driver.find_elements(By.CLASS_NAME, "added-manually")) == 3

    driver.find_element(By.CLASS_NAME, "added-manually").click()
    assert len(driver.find_elements(By.CLASS_NAME, "added-manually")) == 2


def test_tc07_javascript_alerts(driver):
    """TC07: Xử lý JS Alert / Confirm / Prompt."""
    driver.get(f"{BASE_URL}/javascript_alerts")
    result = lambda: driver.find_element(By.ID, "result").text

    # Alert -> OK
    driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
    driver.switch_to.alert.accept()
    assert result() == "You successfully clicked an alert"

    # Confirm -> Cancel
    driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
    driver.switch_to.alert.dismiss()
    assert result() == "You clicked: Cancel"

    # Prompt -> nhập text
    driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
    alert = driver.switch_to.alert
    alert.send_keys("Selenium")
    alert.accept()
    assert result() == "You entered: Selenium"


def test_tc08_dynamic_loading_explicit_wait(driver):
    """TC08: Dùng Explicit Wait chờ nội dung tải động xuất hiện."""
    driver.get(f"{BASE_URL}/dynamic_loading/1")
    driver.find_element(By.CSS_SELECTOR, "#start button").click()

    finish = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4"))
    )
    assert finish.text == "Hello World!"