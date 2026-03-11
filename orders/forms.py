from django import forms

from orders.models import Order


class CheckoutForm(forms.Form):
    payment_method = forms.ChoiceField(
        label='Способ оплаты',
        choices=[
            ('card_mock', 'Банковская карта (муляж)'),
            ('sbp_mock', 'СБП (муляж)'),
            ('cash_mock', 'Наличные при получении (муляж)'),
        ],
    )


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
        labels = {'status': 'Статус заказа'}
