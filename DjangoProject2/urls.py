from django.contrib import admin
from django.urls import path, include  # Обов'язково додай include сюди!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')), # Підключаємо маршрути нашої аплікації
]