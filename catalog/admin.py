from django.contrib import admin

from catalog.models import Category, Product, ProductReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'is_active')
	prepopulated_fields = {'slug': ('name',)}
	list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'stock_quantity', 'is_active', 'updated_at')
	list_filter = ('is_active', 'category')
	search_fields = ('name', 'description')
	prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
	list_display = ('product', 'author', 'rating', 'created_at')
	list_filter = ('rating',)
	search_fields = ('product__name', 'author__username', 'text')

# Register your models here.
