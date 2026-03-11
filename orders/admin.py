from django.contrib import admin

from orders.models import Order, OrderItem, Receipt


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'status', 'total_price', 'created_at')
	list_filter = ('status',)
	search_fields = ('id', 'user__username')
	inlines = (OrderItemInline,)


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
	list_display = ('order', 'created_at', 'deleted_at')
	readonly_fields = ('created_at',)

# Register your models here.
