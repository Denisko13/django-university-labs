from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва товару")
    # Зв'язуємо товар з категорією
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

class Review(models.Model):
    # Зв'язуємо відгук з конкретним товаром
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    author = models.CharField(max_length=100, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст відгуку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return f"Відгук від {self.author}"

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"