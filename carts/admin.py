from django.contrib import admin


from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('id','product','category','product_price','quantity',)
    list_display_links = ('id','product')
    search_fields = ('product','price')
    list_per_page = 25

admin.site.register(Cart, CartAdmin)
