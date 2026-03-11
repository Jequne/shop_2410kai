from django import forms

from catalog.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('text', 'rating')
        labels = {
            'text': 'Ваш отзыв',
            'rating': 'Оценка',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Поделитесь впечатлением о товаре'}),
        }
