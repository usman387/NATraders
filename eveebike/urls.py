import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from website import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('productslist/', views.productslist, name='productslist'),
    path('contact/', views.contact, name='contact'),
    path('productdetail/<int:product_id>/', views.productdetail, name='productdetail'),

    # Cart URLs
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # Additional AJAX endpoints
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('get-cart-total/', views.get_cart_total, name='get_cart_total'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)