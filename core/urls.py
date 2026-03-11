from django.urls import path

from core.views import about_view, close_banner, landing_view, set_view_mode, terms_view

app_name = 'core'

urlpatterns = [
    path('', landing_view, name='landing'),
    path('about/', about_view, name='about'),
    path('terms/', terms_view, name='terms'),
    path('set-view-mode/<str:mode>/', set_view_mode, name='set_view_mode'),
    path('close-banner/', close_banner, name='close_banner'),
]
