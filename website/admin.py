from django.contrib import admin
from django import forms
from .models import (
    Banner, BannerFeature,Product, ProductImage, ProductFAQ, Service, Project,
    Testimonial, BlogPost, SiteSetting, Cart, CartItem, Order, OrderItem
)
# ==================== BANNER FEATURES INLINE ====================
class BannerFeatureInline(admin.TabularInline):
    model = BannerFeature
    extra = 2
    fields = ('title', 'subtitle', 'icon', 'order', 'is_active')
    classes = ('collapse',)
    verbose_name = "Feature"
    verbose_name_plural = "Features"

@admin.register(BannerFeature)
class BannerFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'banner', 'order', 'is_active')
    list_filter = ('banner', 'is_active')
    search_fields = ('title', 'subtitle')
    list_editable = ('order', 'is_active')
# ==================== BANNER ====================
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    inlines = [BannerFeatureInline]


# ==================== PRODUCT ====================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'order')
    classes = ('collapse',)


class ProductFAQInline(admin.TabularInline):
    model = ProductFAQ
    extra = 1
    fields = ('question', 'answer', 'order', 'is_active')
    classes = ('collapse',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductFAQInline]
    list_display = ('name', 'price', 'category', 'tab', 'stock', 'is_featured', 'created_at')
    list_filter = ('category', 'tab', 'is_featured', 'created_at')
    search_fields = ('name', 'description', 'short_description')
    readonly_fields = ('created_at',)
    list_editable = ('price', 'stock', 'is_featured')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'short_description', 'description', 'price', 'image', 'category', 'is_featured', 'tab', 'stock')
        }),
        ('Body Dimensions', {
            'fields': ('length', 'width', 'height', 'seat_height', 'seat_length', 'colors', 'ground_clearance'),
            'classes': ('collapse',)
        }),
        ('Motor Specifications', {
            'fields': ('motor_type', 'rated_power', 'max_torque', 'max_speed', 'controller', 'motor_warranty'),
            'classes': ('collapse',)
        }),
        ('Electrical Specifications', {
            'fields': ('battery_type', 'battery_capacity', 'battery_voltage', 'battery_warranty', 'meter', 'charger',
                       'discharge_time', 'electrical_cost'),
            'classes': ('collapse',)
        }),
        ('Tyres & Brakes', {
            'fields': ('wheel', 'tire_size', 'tire_type', 'shock_front_rear', 'brake_front_rear'),
            'classes': ('collapse',)
        }),
    )


# ==================== SERVICE ====================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


# ==================== PROJECT ====================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'progress_percent')


# ==================== TESTIMONIAL ====================
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')
    list_filter = ('rating',)


# ==================== BLOG ====================
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_featured')
    list_filter = ('is_featured', 'category')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'


# ==================== SITE SETTINGS ====================
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key',)


# ==================== CART ====================
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at', 'get_total_items')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_key')
    readonly_fields = ('created_at', 'updated_at')

    def get_total_items(self, obj):
        return obj.get_total_items()

    get_total_items.short_description = 'Total Items'


# ==================== CART ITEM ====================
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_info', 'product', 'quantity', 'added_at', 'get_subtotal')
    list_filter = ('added_at',)
    search_fields = ('cart__user__username', 'product__name', 'cart__session_key')
    readonly_fields = ('added_at',)

    def get_user_info(self, obj):
        """Get user information from cart"""
        if obj.cart and obj.cart.user:
            return obj.cart.user.username
        elif obj.cart and obj.cart.session_key:
            return f"Session: {obj.cart.session_key[:10]}..."
        return 'Anonymous'

    get_user_info.short_description = 'User'

    def get_subtotal(self, obj):
        return obj.get_subtotal()

    get_subtotal.short_description = 'Subtotal'


# ==================== ORDER ====================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'quantity', 'price', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'get_full_name', 'email', 'phone', 'total', 'payment_method', 'order_status', 'created_at')
    list_filter = ('order_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'order_status', 'payment_status')
        }),
        ('Customer Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Billing Address', {
            'fields': ('company_name', 'country', 'address', 'address2', 'city', 'state', 'postcode')
        }),
        ('Order Details', {
            'fields': ('subtotal', 'shipping_cost', 'discount', 'total', 'payment_method')
        }),
        ('Additional', {
            'fields': ('order_notes', 'created_at', 'updated_at')
        }),
    )

    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']

    def mark_as_processing(self, request, queryset):
        queryset.update(order_status='processing')
    mark_as_processing.short_description = "Mark selected orders as Processing"

    def mark_as_shipped(self, request, queryset):
        queryset.update(order_status='shipped')
    mark_as_shipped.short_description = "Mark selected orders as Shipped"

    def mark_as_delivered(self, request, queryset):
        queryset.update(order_status='delivered')
    mark_as_delivered.short_description = "Mark selected orders as Delivered"


# ==================== ORDER ITEM ====================
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'price', 'subtotal')
    list_filter = ('order',)
    search_fields = ('product_name',)