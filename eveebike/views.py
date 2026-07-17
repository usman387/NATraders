from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Banner, Product, Service, Project, Testimonial, BlogPost, Cart, CartItem, Order, OrderItem
import json
import random
import string


# ==================== HELPER FUNCTIONS ====================
def generate_order_number():
    """Generate unique order number"""
    return 'ORD-' + ''.join(random.choices(string.digits, k=10))


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


# ==================== HOME PAGE VIEWS ====================
def home(request):
    """Home page view"""
    banners = Banner.objects.filter(is_active=True).order_by('order')
    featured_products = Product.objects.filter(is_featured=True)[:4]
    all_products = Product.objects.all()
    products_by_tab = {
        'tab1': all_products.filter(tab='tab1'),
        'tab2': all_products.filter(tab='tab2'),
        'tab3': all_products.filter(tab='tab3'),
    }
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


@login_required
def update_cart(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()

            # Get all cart items for the user
            cart_items = CartItem.objects.filter(cart__user=request.user)
            cart_subtotal = sum(item.get_subtotal() for item in cart_items)
            cart_total = cart_subtotal

            # Prepare items data
            items_data = []
            for item in cart_items:
                items_data.append({
                    'id': item.id,
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'subtotal': float(item.get_subtotal()),
                })

            return JsonResponse({
                'status': 'success',
                'message': 'Cart updated successfully',
                'item_subtotal': float(cart_item.get_subtotal()),
                'cart_subtotal': float(cart_subtotal),
                'cart_total': float(cart_total),
                'cart_count': cart_items.count(),
                'items': items_data
            })
        except CartItem.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Item not found in cart'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            cart_item.delete()

            cart_items = CartItem.objects.filter(cart__user=request.user)
            cart_subtotal = sum(item.get_subtotal() for item in cart_items)

            return JsonResponse({
                'status': 'success',
                'message': 'Item removed from cart',
                'cart_total': float(cart_subtotal),
                'cart_count': cart_items.count(),
                'cart_items': cart_items.count()
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def clear_cart(request):
    """Clear all items from cart"""
    if request.method == 'POST':
        try:
            CartItem.objects.filter(cart__user=request.user).delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Cart cleared successfully'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# ==================== CHECKOUT & ORDERS ====================
def checkout(request):
    """Checkout page view"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to checkout')
        return redirect('login')

    cart_items = CartItem.objects.filter(cart__user=request.user)

    if not cart_items:
        messages.warning(request, 'Your cart is empty. Please add items before checkout.')
        return redirect('productslist')

    cart_total = sum(item.get_subtotal() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'checkout.html', context)


@login_required
def place_order(request):
    """Place order - Save to database and send email"""
    if request.method != 'POST':
        return redirect('checkout')

    try:
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        country = request.POST.get('country')
        address = request.POST.get('address')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        order_notes = request.POST.get('order_notes')
        payment_method = request.POST.get('payment_method', 'cod')

        # Get cart items
        cart_items = CartItem.objects.filter(cart__user=request.user)

        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('cart')

        # Calculate totals
        subtotal = sum(item.get_subtotal() for item in cart_items)
        shipping = 0.00
        total = subtotal + shipping

        # Generate order number
        order_number = generate_order_number()

        # Prepare cart data
        cart_data = {
            'items': [],
            'total': float(total)
        }
        for item in cart_items:
            cart_data['items'].append({
                'id': item.id,
                'name': item.product.name,
                'quantity': item.quantity,
                'price': float(item.product.price),
                'subtotal': float(item.get_subtotal())
            })

        # Create order
        order = Order.objects.create(
            order_number=order_number,
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            country=country,
            address=address,
            address2=address2,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            order_notes=order_notes,
            cart_data=cart_data,
            subtotal=subtotal,
            shipping_cost=shipping,
            total=total,
            payment_method=payment_method,
            order_status='pending'
        )

        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                subtotal=cart_item.get_subtotal()
            )

        # Clear the cart
        cart_items.delete()

        messages.success(request, f'Order #{order_number} placed successfully!')
        return redirect('order_confirmation', order_number=order_number)

    except Exception as e:
        print(f"Error placing order: {str(e)}")
        messages.error(request, f'Error placing order: {str(e)}')
        return redirect('checkout')


@login_required
def order_confirmation(request, order_number):
    """Order confirmation page"""
    try:
        order = Order.objects.get(order_number=order_number, user=request.user)
        context = {
            'order': order,
        }
        return render(request, 'order_confirmation.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('home')


# ==================== COUPON ====================
@login_required
def apply_coupon(request):
    """Apply coupon code"""
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        # Add your coupon logic here
        return JsonResponse({
            'status': 'success',
            'message': 'Coupon applied successfully'
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# ==================== AJAX HELPER VIEWS ====================
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