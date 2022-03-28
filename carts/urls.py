from django.urls import path

from . import views

urlpatterns = [
    path('cart',views.cart,name='cart'),
    path('cartcheckout',views.cartcheckout,name='cartcheckout'),
    path('import_data',views.import_data,name='import_data'),
]