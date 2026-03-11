from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from accounts.models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        user.email = email
        user.username = self._generate_username(email)
        if commit:
            user.save()
        return user

    @staticmethod
    def _generate_username(email):
        base_username = slugify(email.split('@', 1)[0]) or 'user'
        username = base_username[:150]
        suffix = 1

        while User.objects.filter(username=username).exists():
            suffix_str = str(suffix)
            username = f'{base_username[:150 - len(suffix_str) - 1]}-{suffix_str}'
            suffix += 1

        return username


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': 'Введите корректные email и пароль.',
        'inactive': 'Этот аккаунт отключен.',
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise ValidationError(self.error_messages['invalid_login'])
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(self.error_messages['inactive'])

    def get_user(self):
        return self.user_cache


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'address')
        labels = {
            'phone': 'Телефон',
            'address': 'Адрес',
        }
