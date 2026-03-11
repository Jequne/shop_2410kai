from django.urls import path

from catalog.views import add_review_view, product_detail_view, product_list_view

app_name = 'catalog'

urlpatterns = [
    path('', product_list_view, name='product_list'),
    path('<slug:slug>/', product_detail_view, name='product_detail'),
    path('<slug:slug>/review/', add_review_view, name='add_review'),
]
