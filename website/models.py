from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField  # For rich text editing
# from ckeditor_uploader.fields import RichTextUploadingField  # For rich text with image upload


# ==================== BANNER ====================
class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


# ==================== PRODUCT ====================


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class Product(models.Model):
    TAB_CHOICES = [
        ('tab1', 'Okla'),
        ('tab2', 'YJ Future'),
        ('tab3', 'Road King'),
    ]

    # Basic Info
    name = models.CharField(max_length=200)
    short_description = models.TextField(
        blank=True,
        help_text="Brief description for product cards (you can use HTML tags like <b>bold</b> or <ul><li>bullet</li></ul>)"
    )
    description = models.TextField(
        blank=True,
        help_text="Full description with HTML formatting. Use: <b>bold</b>, <ul><li>bullet points</li></ul>, <i>italic</i>, etc."
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    tab = models.CharField(max_length=10, choices=TAB_CHOICES, default='tab1')
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Body Dimensions
    length = models.CharField(max_length=50, blank=True, null=True)
    width = models.CharField(max_length=50, blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)
    seat_height = models.CharField(max_length=50, blank=True, null=True)
    seat_length = models.CharField(max_length=50, blank=True, null=True)
    colors = models.CharField(max_length=200, blank=True, null=True, help_text='Comma-separated')
    ground_clearance = models.CharField(max_length=50, blank=True, null=True)

    # Motor
    motor_type = models.CharField(max_length=100, blank=True, null=True)
    rated_power = models.CharField(max_length=100, blank=True, null=True)
    max_torque = models.CharField(max_length=100, blank=True, null=True)
    max_speed = models.CharField(max_length=100, blank=True, null=True)
    controller = models.CharField(max_length=100, blank=True, null=True)
    motor_warranty = models.CharField(max_length=100, blank=True, null=True)

    # Electricals
    battery_type = models.CharField(max_length=100, blank=True, null=True)
    battery_capacity = models.CharField(max_length=100, blank=True, null=True)
    battery_voltage = models.CharField(max_length=100, blank=True, null=True)
    battery_warranty = models.CharField(max_length=100, blank=True, null=True)
    meter = models.CharField(max_length=100, blank=True, null=True)
    charger = models.CharField(max_length=100, blank=True, null=True)
    discharge_time = models.CharField(max_length=100, blank=True, null=True)
    electrical_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Tyres & Brakes
    wheel = models.CharField(max_length=100, blank=True, null=True)
    tire_size = models.CharField(max_length=100, blank=True, null=True)
    tire_type = models.CharField(max_length=100, blank=True, null=True)
    shock_front_rear = models.CharField(max_length=200, blank=True, null=True)
    brake_front_rear = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_list(self):
        """Return list of colors (trimmed) from comma-separated `colors` field."""
        if not self.colors:
            return []
        return [c.strip() for c in self.colors.split(',') if c.strip()]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('productdetail', args=[str(self.id)])

    def get_description_html(self):
        """Return description as safe HTML"""
        return mark_safe(self.description) if self.description else ''

    def get_short_description_html(self):
        """Return short description as safe HTML"""
        return mark_safe(self.short_description) if self.short_description else ''

    class Meta:
        ordering = ['-created_at']


# ==================== PRODUCT IMAGES ====================
class ProductImage(models.Model):
    """Additional images for a Product."""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} image ({self.id})"

    class Meta:
        ordering = ['order']


# ==================== PRODUCT FAQ ====================
class ProductFAQ(models.Model):
    """Frequently asked questions for a product."""
    product = models.ForeignKey(Product, related_name='faqs', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order']


# ==================== SERVICE ====================
class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to='services/')
    link = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


# ==================== PROJECT ====================
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/')
    progress_percent = models.IntegerField(default=0)
    link = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title


# ==================== TESTIMONIAL ====================
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default=5)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    def __str__(self):
        return self.name


# ==================== BLOG POST ====================
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog/')
    category = models.CharField(max_length=100)
    published_date = models.DateField(default=timezone.now)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# ==================== SITE SETTING ====================
class SiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.key


# ==================== CART ====================
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        """Calculate total cart price"""
        from django.db.models import Sum, F
        total = self.items.aggregate(
            total=Sum(F('product__price') * F('quantity'))
        )['total']
        return total or 0

    def get_total_items(self):
        """Get total number of items in cart"""
        from django.db.models import Sum
        return self.items.aggregate(total=Sum('quantity'))['total'] or 0

    def __str__(self):
        if self.user:
            return f"Cart - {self.user.username}"
        return f"Cart - {self.session_key}"


# ==================== CART ITEM ====================
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        unique_together = ('cart', 'product')  # Prevent duplicate items