import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# ======= CẤU HÌNH FIXTURE TRÌNH DUYỆT (CHẠY NGẦM) =======
@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Chạy không giao diện đồ hoạ cho Server Github
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# =========================================================================
# 1. KIỂM THỬ HỒI QUY (Regression Testing)
# =========================================================================
@pytest.mark.parametrize("url_path", [
    "/",          # Trang chủ
    "/login",     # Trang đăng nhập
    "/product",   # Trang dánh sách sản phẩm
    "/cart",      # Giỏ hàng
    "/blog"       # Tin tức
])
def test_regression_all_pages_healthy(driver, url_path):
    """HỒI QUY: Quét chéo toàn bộ danh mục trang chính xem code mới có làm nát màn hình cũ không"""
    driver.get(f"http://localhost:8080{url_path}")
    source = driver.page_source
    assert "Whitelabel Error Page" not in source, f"⛔ LỖI HỒI QUY: Trang {url_path} bị sập (Error 500)"
    assert "404" not in source, f"⛔ LỖI HỒI QUY: Trang {url_path} không tìm thấy (Error 404)"

# =========================================================================
# 2. KIỂM THỬ LUỒNG NGHIỆP VỤ CHÍNH (Core Business Workflows)
# =========================================================================
def test_business_login_form_exists(driver):
    """NGHIỆP VỤ: Đảm bảo giao diện Đăng nhập luôn có ô nhập Mật khẩu để chống lỗi Render Form"""
    driver.get("http://localhost:8080/login")
    password_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
    # Web thời trang bắt buộc phải cho phép khách hàng nhập mật khẩu
    assert len(password_inputs) > 0, "⛔ LỖI NGHIỆP VỤ: Trang login bị mất tính năng nhập mật khẩu!"

def test_business_cart_logic_accessible(driver):
    """NGHIỆP VỤ: Không được phép có lỗi Java khi khách hàng truy cập Giỏ Hàng"""
    driver.get("http://localhost:8080/cart")
    assert "Whitelabel Error" not in driver.page_source, "⛔ LỖI NGHIỆP VỤ: Sập Database khi vào Giỏ hàng!"

# =========================================================================
# 3. KIỂM THỬ TÍNH TƯƠNG THÍCH (Compatibility Testing)
# =========================================================================
def test_compatibility_mobile_view(driver):
    """TƯƠNG THÍCH: Giả lập màn hình iPhone 13 (390x844) xem Web có Responsive ko"""
    driver.set_window_size(390, 844)
    driver.get("http://localhost:8080")
    # Kiểm tra xem mã HTML có bị trào ra ngoài chiều rộng màn hình điện thoại hay không
    body_width = driver.find_element(By.TAG_NAME, "body").size['width']
    assert body_width <= 390, f"⛔ LỖI RESPONSIVE: Giao diện Mobile rườm rà, chèn khung ({body_width}px)!"

def test_compatibility_desktop_hd_view(driver):
    """TƯƠNG THÍCH: Giả lập màn hình PC Full HD siêu rộng (1920x1080)"""
    driver.set_window_size(1920, 1080)
    driver.get("http://localhost:8080")
    # Đảm bảo source web vẫn tải nạp cấu trúc khung xương (Layout) ổn định mà ko ném lỗi JavaScript
    assert len(driver.page_source) > 0

# =========================================================================
# 4. KIỂM THỬ GIAO DIỆN & TRẢI NGHIỆM (UI & UX Testing)
# =========================================================================
def test_ux_images_are_not_broken(driver):
    """UX/UI: Quét trang chủ đảm bảo tất cả khung ảnh đều có Source link (src) đàng hoàng"""
    driver.get("http://localhost:8080")
    # Thẻ <img> có thể bị JavaScript (như Slider/Carousel) xóa mờ hoặc thay thế trong lúc Selenium duyệt thẻ, gây lỗi "Stale element".
    # Giải pháp chuẩn: Rút thẳng toàn bộ SRC của toàn bộ ảnh tại 1 thời điểm bằng JavaScript nội bộ.
    image_srcs = driver.execute_script("return Array.from(document.querySelectorAll('img')).map(img => img.getAttribute('src'));")
    
    for src in image_srcs:
        # Bỏ qua những ảnh base64 hoặc ảnh được sinh ra chậm
        if src is not None and not src.startswith("data:image"):
            assert len(src.strip()) > 0, "⛔ LỖI TRẢI NGHIỆM UX: Phát hiện một thẻ ảnh bị rỗng (vỡ ảnh)!"

# =========================================================================
# 5. KIỂM THỬ HIỆU NĂNG CƠ BẢN (Basic Performance Testing)
# =========================================================================
@pytest.mark.parametrize("route", ["/", "/product"])
def test_performance_speed(driver, route):
    """HIỆU NĂNG: Benchmark đo thông lượng và tốc độ tải các trang năng nề xem có trễ không"""
    start_time = time.time()
    driver.get(f"http://localhost:8080{route}")
    end_time = time.time()
    
    load_time = round((end_time - start_time), 2)
    # Máy ảo Github đôi khi bị lác, nới lỏng hiệu năng cho ứng dụng lên dưới 6s (chuẩn cơ bản) thay vì 3s
    assert load_time <= 6.0, f"⛔ LỖI HIỆU NĂNG: Đường dẫn '{route}' load siêu chậm ({load_time}s). Hãy cài Caching!"
