from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import resolve_url
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from accounts.forms import EmailAuthenticationForm, ProfileForm, SignUpForm


def signup_view(request):
	if request.user.is_authenticated:
		return redirect('catalog:product_list')
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Регистрация успешно выполнена.')
			return redirect('catalog:product_list')
	else:
		form = SignUpForm()
	return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
	if request.user.is_authenticated:
		return redirect('catalog:product_list')

	form = EmailAuthenticationForm(request, data=request.POST or None)
	if request.method == 'POST' and form.is_valid():
		login(request, form.get_user())
		messages.success(request, 'Вход выполнен.')
		redirect_to = request.POST.get(REDIRECT_FIELD_NAME) or request.GET.get(REDIRECT_FIELD_NAME)
		if redirect_to and url_has_allowed_host_and_scheme(redirect_to, {request.get_host()}, require_https=request.is_secure()):
			return redirect(redirect_to)
		return redirect('catalog:product_list')

	return render(
		request,
		'accounts/login.html',
		{'form': form, 'next': request.POST.get(REDIRECT_FIELD_NAME) or request.GET.get(REDIRECT_FIELD_NAME, '')},
	)


@require_POST
def logout_view(request):
	logout(request)
	messages.success(request, 'Вы вышли из аккаунта.')
	return redirect(resolve_url('core:landing'))


@login_required
def profile_view(request):
	profile = request.user.profile
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			messages.success(request, 'Профиль обновлен.')
			return redirect('accounts:profile')
	else:
		form = ProfileForm(instance=profile)

	orders = request.user.orders.select_related('receipt').all()
	return render(request, 'accounts/profile.html', {'form': form, 'orders': orders})

# Create your views here.
