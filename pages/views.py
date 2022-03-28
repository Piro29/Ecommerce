from django.shortcuts import render
from django.http import HttpResponse
from carts.models import Cart
from products.models import Product
from django.contrib.auth.models import User, Group


def index(request):
    products = Product.objects.order_by('-list_date').filter(is_published=True)[:10]
    # print(request.user.groups.all()[0])

    count = Cart.objects.filter(user_id=request.user.id,is_published=True).count()

    if request.user.is_authenticated:
        if request.user.groups.exists():
            recommend = Product.objects.filter(group=request.user.groups.all()[0])[:10]
            context = {
                'recommend': recommend,
                'products': products,
                'count': count
            }
        else:
            context = {
                'products': products,
                'count': count
            }
    else:
        context = {
            'products': products,
            'count': count
        }

    return render(request, 'pages/index.html', context)


def about(request):
    print(request.user.groups.all())
    return render(request, 'pages/about.html')
