from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def landing_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'core/landing.html')


def about_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'core/about.html')


def terms_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'core/terms.html')


def set_view_mode(request: HttpRequest, mode: str) -> HttpResponse:
	response = redirect(request.GET.get('next') or 'catalog:product_list')
	response.set_cookie('view_mode', mode, max_age=60 * 60 * 24 * 90)
	return response


def close_banner(request: HttpRequest) -> HttpResponse:
	response = redirect(request.GET.get('next') or 'core:landing')
	response.set_cookie('banner_closed', '1', max_age=60 * 60 * 24 * 30)
	return response


def handler403(request: HttpRequest, exception) -> HttpResponse:
	return render(request, 'errors/403.html', status=403)


def handler404(request: HttpRequest, exception) -> HttpResponse:
	return render(request, 'errors/404.html', status=404)


def handler500(request: HttpRequest) -> HttpResponse:
	return render(request, 'errors/500.html', status=500)

# Create your views here.
