from django.urls import path, include
from . import views

app_name = 'website'

urlpatterns = [
    # Main Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('productslist/', views.productslist, name='productslist'),
    path('contact/', views.contact, name='contact'),
    path('productdetail/<int:product_id>/', views.productdetail, name='productdetail'),

    # Cart URLs
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),

    # Coupon
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),

    # AJAX endpoints
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('get-cart-total/', views.get_cart_total, name='get_cart_total'),
]