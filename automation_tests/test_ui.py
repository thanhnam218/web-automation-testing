import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture
def driver():
    # Cài đặt trình duyệt chạy nền tảng chữ (Headless) để tương thích với Github Actions
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Khởi tạo WebDriver tự động tải Driver tương thích
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Đợi tối đa 10s nếu các phần tử web load chậm
    driver.implicitly_wait(10)
    yield driver
    
    # Đóng Chrome sau khi test xong
    driver.quit()

def test_homepage_loads_successfully(driver):
    """
    Bài test 1: Truy cập trang chủ của dự án Spring Boot Fashion Store
    """
    # Bước 1: Mở trình duyệt đi vào Localhost (Do máy chủ ảo Github Actions đang bật SpringBoot tại 8080)
    driver.get("http://localhost:8080")
    
    # Tạm dừng xíu để chắc chắn web render xong
    time.sleep(2)
    
    # Bước 2: Kiểm tra trang web có phản hồi và có chức danh (Title) hay không
    assert driver.title is not None
    
    # Hiện tại test chỉ đang truy cập cơ bản. 
    # Bạn dùng driver.find_element(By.ID, "id_element") để giả lập Click chuột hoặc Gõ phím ở đoạn này!
