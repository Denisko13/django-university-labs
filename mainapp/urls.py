from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),          # Головна сторінка
    path('page1/', views.page1_view, name='page1'),  # Перша сторінка
    path('page2/', views.page2_view, name='page2'),  # Друга сторінка
]