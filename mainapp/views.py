from django.shortcuts import render, get_object_or_404
from .models import Category, Product  # Підключаємо наші таблиці


def home_view(request):
    # Дістаємо всі категорії та товари з бази даних
    categories = Category.objects.all()
    products = Product.objects.all()

    context = {
        'title': 'Головна - Магазин Нічників',
        'categories': categories,  # Передаємо категорії в шаблон
        'products': products,  # Передаємо товари в шаблон
        'is_home': True
    }
    return render(request, 'page.html', context)


def page1_view(request):
    # Для інших сторінок теж передаємо категорії, щоб меню працювало всюди
    categories = Category.objects.all()
    context = {
        'title': 'Про нас',
        'heading': 'Інформація про наш магазин',
        'content': 'Ми продаємо найкращі нічники!',
        'categories': categories,
        'is_home': False
    }
    return render(request, 'page.html', context)


def page2_view(request):
    categories = Category.objects.all()
    context = {
        'title': 'Контакти',
        'heading': 'Зв\'яжіться з нами',
        'content': 'Наш телефон: +380000000000',
        'categories': categories,
        'is_home': False
    }
    return render(request, 'page.html', context)


def category_view(request, category_id):
    categories = Category.objects.all()
    # Шукаємо категорію за її ID
    category = get_object_or_404(Category, id=category_id)
    # Фільтруємо товари: беремо ТІЛЬКИ ті, що належать до цієї категорії
    products = Product.objects.filter(category=category)

    context = {
        'title': f'Категорія: {category.name}',
        'categories': categories,
        'category': category,
        'products': products,
        'is_category': True,  # Прапорець для шаблону
    }
    return render(request, 'page.html', context)


def product_view(request, product_id):
    categories = Category.objects.all()
    # Шукаємо конкретний товар
    product = get_object_or_404(Product, id=product_id)

    context = {
        'title': product.name,
        'categories': categories,
        'product': product,
        'is_product': True,  # Прапорець для сторінки товару
    }
    return render(request, 'page.html', context)