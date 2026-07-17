from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Banner, Product, Service, Project, Testimonial, BlogPost, Cart, CartItem
import json


# ==================== HOME PAGE VIEWS ====================
def home(request):
    # Get all active banners
    banners = Banner.objects.filter(is_active=True).order_by('order')

    # Get featured products (for any other section that needs them)
    featured_products = Product.objects.filter(is_featured=True)[:4]

    # Group ALL products by tab (for the dynamic tabs section)
    all_products = Product.objects.all()
    products_by_tab = {
        'tab1': all_products.filter(tab='tab1'),
        'tab2': all_products.filter(tab='tab2'),
        'tab3': all_products.filter(tab='tab3'),
    }

    # Services, projects, testimonials, blog posts
    services = Service.objects.all().order_by('order')[:6]
    projects = Project.objects.all()[:6]
    testimonials = Testimonial.objects.all()
    blog_posts = BlogPost.objects.order_by('-published_date')[:3]

    context = {
        'banners': banners,
        'featured_products': featured_products,
        'products_by_tab': products_by_tab,
        'services': services,
        'projects': projects,
        'testimonials': testimonials,
        'blog_posts': blog_posts,
    }
    return render(request, 'index.html', context)


# ==================== STATIC PAGE VIEWS ====================
def about(request):
    return render(request, 'about.html')


def productslist(request):
    products = Product.objects.all()
    return render(request, 'productlist.html', {'products': products})


def contact(request):
    return render(request, 'contact.html')


def productdetail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'productdetail.html', {'product': product})


def checkout(request):
    return render(request, 'checkout.html')


# ==================== CART HELPER FUNCTIONS ====================
def get_or_create_cart(request):
    """Get or create a cart for the current user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # For anonymous users, use session
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


# ==================== CART VIEWS ====================
def cart(request):
    """Display cart page"""
    cart_obj = None
    cart_items = []
    cart_total = 0

    if request.user.is_authenticated:
        try:
            cart_obj = Cart.objects.get(user=request.user)
            cart_items = cart_obj.items.all().select_related('product')
            cart_total = cart_obj.get_total()
        except Cart.DoesNotExist:
            pass
    else:
        session_key = request.session.session_key
        if session_key:
            try:
                cart_obj = Cart.objects.get(session_key=session_key)
                cart_items = cart_obj.items.all().select_related('product')
                cart_total = cart_obj.get_total()
            except Cart.DoesNotExist:
                pass

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_obj': cart_obj,
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        cart = get_or_create_cart(request)

        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, f'{product.name} added to cart!')

        # Check if request is AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': f'{product.name} added to cart!',
                'cart_total': float(cart.get_total()),
                'cart_items': cart.get_total_items()
            })

        return redirect('cart')

    return redirect('productslist')


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()

        messages.success(request, 'Item removed from cart!')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Item removed from cart!',
                'cart_total': float(cart.get_total()),
                'cart_items': cart.get_total_items()
            })

        return redirect('cart')
    return redirect('cart')


def update_cart_quantity(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        new_quantity = int(request.POST.get('quantity', 1))

        if new_quantity <= 0:
            cart_item.delete()
            message = 'Item removed from cart!'
            item_subtotal = 0
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            message = 'Cart updated successfully!'
            item_subtotal = cart_item.product.price * cart_item.quantity

        cart_total = cart.get_total()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': message,
                'cart_total': float(cart_total),
                'cart_items': cart.get_total_items(),
                'item_subtotal': float(item_subtotal),
                'item_total': float(cart_total)
            })

        messages.success(request, message)
        return redirect('cart')

    return redirect('cart')


def clear_cart(request):
    """Clear all items from cart"""
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        messages.success(request, 'Cart cleared!')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Cart cleared!',
                'cart_total': 0,
                'cart_items': 0
            })

        return redirect('cart')
    return redirect('cart')


# ==================== ADDITIONAL HELPER VIEWS ====================
def get_cart_count(request):
    """Get cart item count (for AJAX calls)"""
    cart = get_or_create_cart(request)
    return JsonResponse({
        'cart_items': cart.get_total_items(),
        'cart_total': float(cart.get_total())
    })


def get_cart_total(request):
    """Get cart total (for AJAX calls)"""
    cart = get_or_create_cart(request)
    return JsonResponse({
        'cart_total': float(cart.get_total()),
        'cart_items': cart.get_total_items()
    })