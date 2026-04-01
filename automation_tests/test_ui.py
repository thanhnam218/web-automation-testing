import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Chạy không giao diện đồ hoạ cho Server Github
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Khởi tạo Selenium Manager (Webdriver tự động 100%)
    driver = webdriver.Chrome(options=chrome_options)
    
    # Thời gian đợi tìm thẻ HTML tối đa nếu chưa render kịp
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# ======= KỊCH BẢN 1: TÌM LỖI CHẾT SERVER (HTTP 500 / 404) TRÊN TRANG CHỦ =======
def test_homepage_healthy(driver):
    """Kiểm tra trang chủ không bị văng lỗi Whitelabel Spring Boot hoặc sập Database"""
    driver.get("http://localhost:8080")
    
    # Rút toàn bộ Source code Web mà trình duyệt nhìn thấy
    page_source = driver.page_source
    
    # Bắt (Assert) những cảnh báo lỗi kinh điển nhất của Spring Boot:
    assert "Whitelabel Error Page" not in page_source, "⛔ [LỖI NGHIÊM TRỌNG]: Trang chủ đã bị sập (HTTP 500) hoặc lỗi Database!"
    assert "This application has no explicit mapping for /error" not in page_source, "⛔ [LỖI ĐỊNH TUYẾN]: Thiếu file Controller cho trang chủ (HTTP 404)!"

# ======= KỊCH BẢN 2: ÉP TẢI TRANG 'ĐĂNG NHẬP' (ROUTING CHECK) =======
def test_login_page_renders_without_crash(driver):
    """Thử nghiệm Router của khách hàng: Trang Web có trỏ đúng vào tính năng login không"""
    driver.get("http://localhost:8080/login")
    page_source = driver.page_source
    
    assert "Whitelabel Error Page" not in page_source, "⛔ [LỖI BACKEND]: Không thể truy cập trang Đăng nhập /login."

# ======= KỊCH BẢN 3: KIỂM TOÁN TỐC ĐỘ (PERFORMANCE CHECK) =======
def test_performance_load_time(driver):
    """Đảm bảo trang Web không bị đứng khung bắt khách hàng chờ quá lâu"""
    start_time = time.time()
    driver.get("http://localhost:8080")
    end_time = time.time()
    
    load_time = round((end_time - start_time), 2)
    # Lượng hoá: Chấp nhận web tải dưới 3.5 giây trên cấu hình Server cục bộ
    assert load_time <= 3.5, f"⚠️ [CẢNH BÁO OPTIMIZE]: Backend/API chạy quá chậm mất {load_time}s! Vui lòng tối ưu lại Query SQL!"

# ======= KỊCH BẢN 4: TEST GIAO DIỆN (UI INTEGRITY) MÙ =======
def test_ui_content_not_empty(driver):
    """Test xem sau khi Web kết xuất HTML thì có thẻ rỗng nào mà không có data không"""
    driver.get("http://localhost:8080")
    
    # Lấy toàn bộ Text hiển thị trên web
    visible_text = driver.find_element(By.TAG_NAME, "body").text
    
    # Nếu Text bằng trống trơn nghĩa là giao diện bị trắng xoá (White Screen of Death ở JS Framework) hoặc HTML rỗng.
    assert len(visible_text) > 0, "⛔ [LỖI FRONTEND]: Giao diện bị trắng xoá! Có thể do sập JavaScript hoặc thiếu template HTML."
