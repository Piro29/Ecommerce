from django.contrib import admin
from . models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title','is_published','size','price','category','list_date','gender')
    list_display_links = ('id','title')
    list_filter = ('category','gender','size')
    list_editable = ('is_published',)
    search_fields = ('title','descriptions','size')
    list_per_page = 25

admin.site.register(Product,ProductAdmin)