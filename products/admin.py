from django.contrib import admin
from .models import Product, Offer


class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'discount')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'image_url')


admin.site.register(Offer, OfferAdmin)


admin.site.register(Product, ProductAdmin)
