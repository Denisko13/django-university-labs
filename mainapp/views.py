from django.shortcuts import render
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