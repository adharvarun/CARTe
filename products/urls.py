from django.urls import path
from .views import index, add_to_cart, get_cart_count, view_cart, remove_from_cart, get_cart_total
from . import views

urlpatterns = [
    path('', index, name='product_list'),
    path('new/', index, name='new_products'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/count/', get_cart_count, name='get_cart_count'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/total/', get_cart_total, name='get_cart_total'),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout")
]
