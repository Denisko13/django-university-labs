from django.contrib import admin
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Виводимо назву, створено о, оновлено о
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at', 'updated_at')
    list_filter = ('category',) # Додаємо фільтр по категоріям для зручності

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'created_at', 'updated_at')