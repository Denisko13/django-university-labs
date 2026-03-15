from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('page1/', views.page1_view, name='page1'),
    path('page2/', views.page2_view, name='page2'),
    # Нові шляхи для Лаби 6:
    path('category/<int:category_id>/', views.category_view, name='category_detail'),
    path('product/<int:product_id>/', views.product_view, name='product_detail'),
]