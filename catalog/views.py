from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from catalog.forms import ProductReviewForm
from catalog.models import Product
from orders.models import OrderItem


def _can_user_review_product(user, product) -> bool:
	if not user.is_authenticated:
		return False
	has_delivered_order = OrderItem.objects.filter(
		order__user=user,
		order__status='DELIVERED',
		product=product,
	).exists()
	has_review = product.reviews.filter(author=user).exists()
	return has_delivered_order and not has_review


def product_list_view(request: HttpRequest) -> HttpResponse:
	q = request.GET.get('q', '').strip()
	category_slug = request.GET.get('category', '').strip()
	sort = request.GET.get('sort', 'new')

	products = Product.objects.filter(is_active=True).select_related('category')
	if q:
		products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
	if category_slug:
		products = products.filter(category__slug=category_slug)

	if sort == 'price':
		products = products.order_by('price')
	elif sort == '-price':
		products = products.order_by('-price')
	else:
		products = products.order_by('-created_at')

	paginator = Paginator(products, 8)
	page_obj = paginator.get_page(request.GET.get('page', 1))

	context = {
		'page_obj': page_obj,
		'q': q,
		'sort': sort,
		'selected_category': category_slug,
	}

	if request.htmx:
		return render(request, 'catalog/partials/product_list_block.html', context)
	return render(request, 'catalog/product_list.html', context)


def product_detail_view(request: HttpRequest, slug: str) -> HttpResponse:
	cache_key = f'product_detail_{slug}'
	product = cache.get(cache_key)
	if not product:
		product = get_object_or_404(Product.objects.select_related('category'), slug=slug, is_active=True)
		cache.set(cache_key, product, 60)

	reviews = product.reviews.select_related('author').all()
	form = ProductReviewForm()

	context = {
		'product': product,
		'reviews': reviews,
		'review_form': form,
		'can_review': _can_user_review_product(request.user, product),
	}
	return render(request, 'catalog/product_detail.html', context)


@login_required
def add_review_view(request: HttpRequest, slug: str) -> HttpResponse:
	if request.method != 'POST':
		return redirect('catalog:product_detail', slug=slug)

	product = get_object_or_404(Product, slug=slug, is_active=True)
	if not _can_user_review_product(request.user, product):
		messages.error(request, 'Оставить отзыв можно только после покупки и доставки товара.')
		return redirect('catalog:product_detail', slug=slug)

	form = ProductReviewForm(request.POST)
	if form.is_valid():
		review = form.save(commit=False)
		review.author = request.user
		review.product = product
		review.save()
		messages.success(request, 'Отзыв успешно добавлен.')
	else:
		messages.error(request, 'Проверьте корректность данных формы отзыва.')

	if request.htmx:
		reviews = product.reviews.select_related('author').all()
		return render(request, 'catalog/partials/reviews_list.html', {'product': product, 'reviews': reviews})

	return redirect('catalog:product_detail', slug=slug)

# Create your views here.
