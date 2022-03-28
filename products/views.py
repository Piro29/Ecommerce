from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .choices import size_choices, price_choices, gender_choices, category_choices, color_choices
from carts.models import Cart



def index(request):
    products = Product.objects.order_by('-list_date').filter(is_published = True)

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    page_products = paginator.get_page(page)
    count = Cart.objects.filter(user_id=request.user.id, is_published=True).count()


    context = {
        'products': page_products,
        'size_choices': size_choices,
        'price_choices': price_choices,
        'gender_choices': gender_choices,
        'category_choices': category_choices,
        'color_choices': color_choices,
        'count': count

    }
    return render(request, 'products/products.html', context)


def product(request, product_id):
    category = Product.objects.get(id=product_id).category
    products = Product.objects.order_by('-list_date').filter(is_published=True, category = category)
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    page_products = paginator.get_page(page)
    product = get_object_or_404(Product, pk=product_id)
    count = Cart.objects.filter(user_id=request.user.id, is_published=True).count()
    print(products)

    context = {
        'product': product,
        'products': page_products,
        'count': count

    }
    return render(request, 'products/product-detail.html', context)


def search(request):
    queryset_list = Product.objects.order_by('-list_date')

    paginator = Paginator(queryset_list, 6)
    page = request.GET.get('page')
    page_products = paginator.get_page(page)
    count = Cart.objects.filter(user_id=request.user.id, is_published=True).count()


    #search-product
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            page_products = queryset_list.filter(title__icontains = keywords)

    #gender
    if 'gender' in request.GET:
        gender = request.GET['gender']
        if gender:
            page_products = queryset_list.filter(gender__iexact = gender)

    #category
    if 'category' in request.GET:
        category = request.GET['category']
        print(category)
        if category:
            page_products = queryset_list.filter(category = category)

    # price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            page_products = queryset_list.filter(price__lte=price)

    # size
    if 'size' in request.GET:
        size = request.GET['size']
        if size:
            page_products = queryset_list.filter(size__iexact=size)



    context = {
        'size_choices': size_choices,
        'price_choices': price_choices,
        'gender_choices': gender_choices,
        'category_choices': category_choices,
        'color_choices': color_choices,
        'products' : page_products,
        'values': request.GET,
        'count': count
    }
    return render(request, 'products/search.html',context)
