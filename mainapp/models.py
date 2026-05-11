from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


# mainapp/models.py

class Product(models.Model):
    name = models.CharField(max_length=200) # Перевір, чи є цей рядок
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=10) # Те, що ми додавали
    created_at = models.DateTimeField(auto_now_add=True) # Перевір наявність
    updated_at = models.DateTimeField(auto_now=True)   # Перевір наявність

    def __str__(self):
        return self.name

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

class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Електронна пошта")
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Order(models.Model):
    # Поки що дозволяємо кошику бути без користувача (null=True), але для 8-ї лаби це знадобиться
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Користувач")
    session_key = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ключ сесії (для неавторизованих)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    is_completed = models.BooleanField(default=False, verbose_name="Оформлено (True = Замовлення, False = Кошик)")
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Прізвище")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    address = models.TextField(blank=True, null=True, verbose_name="Адреса")

    def __str__(self):
        return f"Кошик/Замовлення #{self.id}"

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    # Рахуємо загальну суму кошика
    def get_total_price(self):
        return sum(item.get_total() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    def __str__(self):
        return f"{self.quantity} шт. - {self.product.name}"

    # Рахуємо суму для конкретного товару (ціна * кількість)
    def get_total(self):
        return self.product.price * self.quantity
# mainapp/models.py
