from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('info/', views.page1_view, name='info'),
    path('contacts/', views.page2_view, name='contacts'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('product/<int:product_id>/', views.product_view, name='product'),

    # Наш новий шлях для підписки (перевір чи є кома в кінці!)
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('change-quantity/<int:item_id>/<str:action>/', views.change_quantity, name='change_quantity'),
    path('checkout/', views.checkout, name='checkout'),
]