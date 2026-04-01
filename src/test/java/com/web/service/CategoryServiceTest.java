package com.web.service;

import com.web.entity.Category;
import com.web.exception.MessageException;
import com.web.repository.CategoryRepository;
import com.web.serviceImp.CategoryServiceImp;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import static org.mockito.Mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Optional;

@ExtendWith(MockitoExtension.class)
class CategoryServiceTest {

    // 1. Tạo Repository giả
    @Mock
    private CategoryRepository categoryRepository;

    // 2. Tiêm Repo giả vào Service thật
    @InjectMocks
    private CategoryServiceImp categoryService;

    @Test
    void save_NenNemRaLoi_KhiIdDaTonTaiKhacNull() {
        // Arrange (Chuẩn bị)
        Category category = new Category();
        category.setId(1L);

        // Act & Assert (Hành động & Kiểm tra ngoại lệ)
        MessageException exception = assertThrows(MessageException.class, () -> {
            categoryService.save(category);
        });
        
        // Kiểm tra xem Service có trả ra đúng thông báo bắt lỗi như code gốc hay không
        assertEquals("Id must null", exception.getMessage());
    }

    @Test
    void save_NenLuuThanhCong_KhiCategoryHopLe() {
        // Arrange (Chuẩn bị dữ liệu đầu vào)
        Category category = new Category();
        category.setName("Áo Thun");

        // Mô phỏng hàm findByName: Giả vờ là cái Name này chưa ai tạo (Optional rỗng)
        when(categoryRepository.findByName("Áo Thun")).thenReturn(Optional.empty());

        Category savedCategory = new Category();
        savedCategory.setId(1L);
        savedCategory.setName("Áo Thun");
        
        // Mô phỏng hàm save: Khi lưu thì trả về thực thể đã có ID
        when(categoryRepository.save(category)).thenReturn(savedCategory);

        // Act (Thực thi hàm save thật của Service)
        Category result = categoryService.save(category);

        // Assert (Đánh giá kết quả nhận được)
        assertNotNull(result);
        assertEquals(1L, result.getId());
        assertEquals("Áo Thun", result.getName());
        
        // Xác minh chắc chắn là hàm save của Repository giả đã được Service gọi 1 lần
        verify(categoryRepository, times(1)).save(category);
    }
}
