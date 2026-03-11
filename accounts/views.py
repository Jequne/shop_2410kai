from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.forms import ProfileForm, SignUpForm


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
