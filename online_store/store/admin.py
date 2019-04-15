from django.contrib import admin
from .models import Product, ProductImage, Transaction, Coupon


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction)
admin.site.register(Coupon)
