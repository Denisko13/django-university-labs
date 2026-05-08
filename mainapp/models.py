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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

    # ДОДАНО ПОЛЕ ОПИСУ (щоб воно підтягувалося на сторінку)
    description = models.TextField(verbose_name="Опис товару", blank=True, null=True)

    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Фотографія")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


class Review(models.Model):
    # ДОДАНО related_name='reviews', щоб працювало product.reviews.all
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Товар")
    author = models.CharField(max_length=100, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст відгуку")

    # ДОДАНО РЕЙТИНГ (для зірочок)
    rating = models.PositiveIntegerField(default=5, verbose_name="Рейтинг (1-5)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return f"Відгук від {self.author} на {self.product.name}"

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"