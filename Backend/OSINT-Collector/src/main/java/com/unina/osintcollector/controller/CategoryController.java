package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Category;
import com.unina.osintcollector.model.Username;
import com.unina.osintcollector.repository.CategoryRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/categories")
public class CategoryController {

    private final CategoryRepository categoryRepository;

    public CategoryController(CategoryRepository categoryRepository) {
        this.categoryRepository = categoryRepository;
    }

    @GetMapping(value = { "/", "" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<Category> getCategories() {
        return categoryRepository.findAll();
    }

}
