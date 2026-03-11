from django import forms


class CartItemUpdateForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Количество')
