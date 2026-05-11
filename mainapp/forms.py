from django import forms
from .models import Review, Newsletter  # Обов'язково імпортуємо ОБИДВІ моделі!

# 1. Форма для відгуків
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'rating', 'text']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ваше ім'я"}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'value': 5}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Напишіть ваш відгук...'}),
        }

# 2. Форма для розсилки (якої зараз не вистачає)
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш Email для новин...'
            }),
        }
from django import forms

class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="Ім'я")
    last_name = forms.CharField(max_length=50, label="Прізвище")
    phone = forms.CharField(max_length=20, label="Телефон")
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Адреса доставки")