from django.shortcuts import render

def home_view(request):
    context = {
        'title': 'Головна',
        'heading': 'Ласкаво просимо на Головну сторінку!',
        'content': 'Це головна сторінка нашого проєкту.',
        'is_home': True
    }
    return render(request, 'page.html', context)

def page1_view(request):
    context = {
        'title': 'Сторінка 1',
        'heading': 'Це Перша сторінка',
        'content': 'Контент першої сторінки, переданий через контекст.',
        'is_home': False
    }
    return render(request, 'page.html', context)

def page2_view(request):
    context = {
        'title': 'Сторінка 2',
        'heading': 'Це Друга сторінка',
        'content': 'Тут знаходиться інформація для другої сторінки.',
        'is_home': False
    }
    return render(request, 'page.html', context)