from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Product, Category, Review, Newsletter, Order, OrderItem
from .forms import ReviewForm, NewsletterForm, OrderForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Створюємо кастомну форму, яка додає поле email
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Електронна пошта")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

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
    return render(request, 'info.html', {'title': 'Про нас', 'heading': 'Інформація про наш магазин',
                                         'content': 'Ми продаємо найкращі нічники!', 'categories': categories,
                                         'is_home': False})


def page2_view(request):
    categories = Category.objects.all()
    return render(request, 'info.html',
                  {'title': 'Контакти', 'heading': 'Зв\'яжіться з нами', 'content': 'Наш телефон: +380000000000',
                   'categories': categories, 'is_home': False})


def category_view(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'home.html',
                  {'title': f'Категорія: {category.name}', 'categories': categories, 'category': category,
                   'products': products, 'is_category': True})


def product_view(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.product = product
            new_review.author = request.user.username if request.user.is_authenticated else form.cleaned_data.get(
                'author', 'Анонім')
            new_review.save()
            return redirect(request.path)
    else:
        form = ReviewForm()

    return render(request, 'product.html',
                  {'title': product.name, 'categories': categories, 'product': product, 'is_product': True,
                   'avg_rating': avg_rating, 'form': form})


def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Дякуємо! Ви успішно підписалися на наші новини 🌙')
        else:
            messages.error(request, 'Цей Email вже підписаний на розсилку, або введено некоректні дані.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    order, created = Order.objects.get_or_create(session_key=session_key, is_completed=False)
    order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)

    current_in_cart = order_item.quantity if not item_created else 0
    new_total = current_in_cart + quantity

    if new_total > product.stock:
        order_item.quantity = product.stock
        messages.warning(request, f"Додано максимально можливу кількість: {product.stock} шт.")
    else:
        order_item.quantity = new_total
        messages.success(request, f"Додано {quantity} шт. у кошик.")

    order_item.save()
    return redirect('cart')


def cart_view(request):
    categories = Category.objects.all()
    session_key = request.session.session_key
    order = Order.objects.filter(session_key=session_key, is_completed=False).first()
    return render(request, 'cart.html', {'order': order, 'categories': categories, 'title': 'Мій кошик'})


def change_quantity(request, item_id, action):
    item = get_object_or_404(OrderItem, id=item_id)
    product = item.product

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

@login_required  # Додаємо цей декоратор
def checkout(request):
    session_key = request.session.session_key
    # ... далі весь твій код без змін ...
def checkout(request):
    session_key = request.session.session_key
    order = Order.objects.filter(session_key=session_key, is_completed=False).first()

    if not order or order.items.count() == 0:
        return redirect('home')

    categories = Category.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.address = form.cleaned_data['address']

            # ПРИВ'ЯЗКА ЗАМОВЛЕННЯ ДО ЮЗЕРА (ДЛЯ 8 ЛАБИ)
            if request.user.is_authenticated:
                order.user = request.user

            for item in order.items.all():
                product = item.product
                product.stock -= item.quantity
                product.save()

            order.is_completed = True
            order.save()
            request.session.create()

            messages.success(request, "Дякуємо! Ваше замовлення прийнято.")
            return render(request, 'success.html', {'categories': categories})
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form, 'order': order, 'categories': categories})


# ==========================================
# ФУНКЦІЇ ДЛЯ ЛАБОРАТОРНОЇ 8
# ==========================================

def register(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        # Використовуємо нашу нову форму з емейлом
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Вітаємо, {user.username}! Ви успішно зареєструвалися.")
            return redirect('home')
    else:
        # І тут теж замінюємо на нову форму
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form, 'categories': categories})


@login_required  # Доступ тільки для авторизованих
def profile(request):
    categories = Category.objects.all()

    # Якщо це адмін - бачить всі замовлення, якщо юзер - тільки свої
    if request.user.is_superuser:
        orders = Order.objects.filter(is_completed=True).order_by('-created_at')
        title = "Всі замовлення (Панель Адміністратора)"
    else:
        orders = Order.objects.filter(user=request.user, is_completed=True).order_by('-created_at')
        title = "Мій особистий кабінет"

    return render(request, 'profile.html', {'orders': orders, 'categories': categories, 'title': title})