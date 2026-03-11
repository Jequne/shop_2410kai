from django import forms

from catalog.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update(
            {
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Поделитесь впечатлением о товаре',
            }
        )
        self.fields['rating'].widget.attrs.update(
            {
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'step': 1,
                'placeholder': 'От 1 до 5',
            }
        )

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
