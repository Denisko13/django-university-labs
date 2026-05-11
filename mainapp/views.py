from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Category, Product
from .forms import ReviewForm, NewsletterForm
from django.contrib import messages
# Знайди цей рядок зверху і переконайся, що там є Order та OrderItem
from .models import Product, Category, Review, Newsletter, Order, OrderItem
# Знайди цей рядок зверху і додай OrderForm у кінець
from .forms import ReviewForm, NewsletterForm, OrderForm


def home_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    context = {
        'title': 'Головна - Магазин Нічників',
        'categories': categories,
        'products': products,
        'is_home': True
    }
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
    return render(request, 'home.html', context)


# === ОБ'ЄДНАНА І ГОТОВА ФУНКЦІЯ ДЛЯ СТОРІНКИ ТОВАРУ ===
def product_view(request, product_id):
    # Дістаємо категорії для меню і сам товар
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)

    # 1. РАХУЄМО СЕРЕДНІЙ БАЛ
    avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0

    # 2. ОБРОБКА ФОРМИ ВІДГУКУ
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.product = product
            new_review.save()
            # Перенаправляємо користувача на цю ж сторінку після відправки
            return redirect(request.path)
    else:
        form = ReviewForm()

    # 3. ПЕРЕДАЄМО ВСІ ДАНІ В HTML
    context = {
        'title': product.name,
        'categories': categories,
        'product': product,
        'is_product': True,
        'avg_rating': avg_rating,  # Передаємо бал
        'form': form  # Передаємо форму
    }

    # Увага: переконайся, що твій HTML файл називається саме 'product.html'
    # (якщо він називається 'product_detail.html', то зміни тут назву)
    return render(request, 'product.html', context)


def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            # Додаємо повідомлення про успіх!
            messages.success(request, 'Дякуємо! Ви успішно підписалися на наші новини 🌙')
        else:
            # Якщо такий емейл вже є в базі
            messages.error(request, 'Цей Email вже підписаний на розсилку, або введено некоректні дані.')

    # Повертаємо користувача на ту сторінку, з якої він відправив форму
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Використовуємо сесію, щоб кошик працював навіть без входу в аккаунт
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Шукаємо незавершене замовлення (кошик) для цієї сесії
    order, created = Order.objects.get_or_create(
        session_key=session_key,
        is_completed=False
    )

    # Перевіряємо, чи є вже цей товар у кошику
    order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)

    if not item_created:
        order_item.quantity += 1  # Якщо вже є — просто додаємо +1 до кількості
        order_item.save()

    messages.success(request, f'Нічник "{product.name}" додано до кошика! 🌙')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def cart_view(request):
    categories = Category.objects.all()
    session_key = request.session.session_key

    # Шукаємо поточний кошик
    order = Order.objects.filter(session_key=session_key, is_completed=False).first()

    return render(request, 'cart.html', {
        'order': order,
        'categories': categories,
        'title': 'Мій кошик'
    })


def change_quantity(request, item_id, action):
    item = get_object_or_404(OrderItem, id=item_id)

    if action == 'plus':
        item.quantity += 1
    elif action == 'minus':
        if item.quantity > 1:
            item.quantity -= 1
        else:
            item.delete()  # Якщо зменшили до 0 — видаляємо товар
            return redirect('cart')

    item.save()
    return redirect('cart')


# mainapp/views.py
# mainapp/views.py

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    # Логіка кошика
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    order, created = Order.objects.get_or_create(session_key=session_key, is_completed=False)
    order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)

    # ПЕРЕВІРКА ЗАПАСУ:
    current_in_cart = order_item.quantity if not item_created else 0
    new_total = current_in_cart + quantity

    if new_total > product.stock:
        order_item.quantity = product.stock # Ставимо максимум, що є
        messages.warning(request, f"Додано максимально можливу кількість: {product.stock} шт.")
    else:
        order_item.quantity = new_total
        messages.success(request, f"Додано {quantity} шт. у кошик.")

    order_item.save()
    return redirect('cart')


# mainapp/views.py

def change_quantity(request, item_id, action):
    item = get_object_or_404(OrderItem, id=item_id)
    product = item.product  # Отримуємо товар, щоб знати його stock

    if action == 'plus':
        if item.quantity < product.stock:
            item.quantity += 1
            item.save()
        else:
            messages.warning(request, f"Вибачте, більше ніж {product.stock} шт. немає в наявності.")

    elif action == 'minus':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    return redirect('cart')


# Переконайся, що зверху є імпорт: from .models import Category

def checkout(request):
    session_key = request.session.session_key
    order = Order.objects.filter(session_key=session_key, is_completed=False).first()

    if not order or order.items.count() == 0:
        return redirect('home')

    # Отримуємо всі категорії для меню
    categories = Category.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.address = form.cleaned_data['address']

            # Списуємо товар зі складу
            for item in order.items.all():
                product = item.product
                product.stock -= item.quantity
                product.save()

            order.is_completed = True
            order.save()

            request.session.create()

            messages.success(request, "Дякуємо! Ваше замовлення прийнято.")
            # Передаємо категорії і на сторінку успіху
            return render(request, 'success.html', {'categories': categories})
    else:
        form = OrderForm()

    # Додали 'categories': categories у словник
    return render(request, 'checkout.html', {'form': form, 'order': order, 'categories': categories})