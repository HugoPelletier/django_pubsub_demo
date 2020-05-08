from django.contrib import admin

# Register your models here.

from .models import Product, Brand, Category, Skus


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class SkusAdmin(admin.ModelAdmin):
    list_display = ['sku']


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Skus, SkusAdmin)
