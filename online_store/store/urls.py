from django.urls import path, include

from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.get_cart, name='cart'),
    path('product/<int:pk>/', views.product, name='product'),
    path('checkout/', views.checkout, name='checkout')
]
