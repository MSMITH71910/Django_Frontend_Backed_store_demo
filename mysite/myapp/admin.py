from django.contrib import admin
from .models import Product, UserProfile, Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_amount')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Order, OrderAdmin)