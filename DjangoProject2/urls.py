from django.contrib import admin
from django.urls import path, include
from django.conf import settings             # Додаємо імпорт налаштувань
from django.conf.urls.static import static   # Додаємо інструмент для статики

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
]

# Додаємо цей рядок, щоб картинки працювали в браузері
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)