from django.shortcuts import render, get_object_or_404
from .models import Category, Product  # Підключаємо наші таблиці


def home_view(request):
    # Дістаємо всі категорії та товари з бази даних
    categories = Category.objects.all()
    products = Product.objects.all()

    context = {
        'title': 'Головна - Магазин Нічників',
        'categories': categories,
        'products': products,
        'is_home': True
    }
    # Змінили 'page.html' на 'home.html'
    return render(request, 'home.html', context)


def page1_view(request):
    categories = Category.objects.all()
    context = {
        'title': 'Про нас',
        'heading': 'Інформація про наш магазин',
        'content': 'Ми продаємо найкращі нічники!',
        'categories': categories,
        'is_home': False
    }
    # Змінили 'page.html' на 'info.html'
    return render(request, 'info.html', context)


def page2_view(request):
    categories = Category.objects.all()
    context = {
        'title': 'Контакти',
        'heading': 'Зв\'яжіться з нами',
        'content': 'Наш телефон: +380000000000',
        'categories': categories,
        'is_home': False
    }
    # Змінили 'page.html' на 'info.html'
    return render(request, 'info.html', context)


def category_view(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    context = {
        'title': f'Категорія: {category.name}',
        'categories': categories,
        'category': category,
        'products': products,
        'is_category': True,
    }
    # Оскільки тут теж список товарів, використовуємо 'home.html'
    return render(request, 'home.html', context)


def product_view(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)

    context = {
        'title': product.name,
        'categories': categories,
        'product': product,
        'is_product': True,
    }
    # Змінили 'page.html' на 'product.html'
    return render(request, 'product.html', context)