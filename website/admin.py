from django.contrib import admin
from django import forms
from .models import Banner, Product, ProductImage, ProductFAQ, Service, Project, Testimonial, BlogPost, SiteSetting, \
    Cart, CartItem


# If you're using CKEditor (uncomment if you have it installed)
# from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Register Banner
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)


# Product Image Inline
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'order')
    classes = ('collapse',)


# Product FAQ Inline
class ProductFAQInline(admin.TabularInline):
    model = ProductFAQ
    extra = 1
    fields = ('question', 'answer', 'order', 'is_active')
    classes = ('collapse',)


# Product Admin with CKEditor support (if you have CKEditor installed)
# Option 1: With CKEditor (uncomment if you have CKEditor installed)
"""
class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    short_description = forms.CharField(widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Product
        fields = '__all__'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
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
            'fields': ('battery_type', 'battery_capacity', 'battery_voltage', 'battery_warranty', 'meter', 'charger', 'discharge_time', 'electrical_cost'),
            'classes': ('collapse',)
        }),
        ('Tyres & Brakes', {
            'fields': ('wheel', 'tire_size', 'tire_type', 'shock_front_rear', 'brake_front_rear'),
            'classes': ('collapse',)
        }),
    )
"""


# Option 2: Without CKEditor (Simple TextField) - Use this if CKEditor is not installed
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
            'fields': ('name', 'short_description', 'description', 'price', 'image', 'category', 'is_featured', 'tab',
                       'stock')
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


# Register other models
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'progress_percent')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')
    list_filter = ('rating',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_featured')
    list_filter = ('is_featured', 'category')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key',)


# Register Cart models if needed
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_key')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('product__name',)