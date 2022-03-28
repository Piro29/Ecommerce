from django.shortcuts import render, redirect
from .models import Cart
from django.contrib import messages
from django.db import connection
from pandas import read_csv
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from django.contrib.auth.models import User
from django.contrib.auth.models import Group



def cart(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        product = request.POST['product']
        name = request.POST['name']
        product_price = request.POST['product_price']
        user_id = request.POST['user_id']
        quantity = request.POST['quantity']
        category = request.POST['category']
        photo = request.POST['photo']

        category_choices = {
            '1': 'Denim',
            '2': 'Pants',
            '3': 'Shorts',
            '4': 'Sweater',
            '5': 'Tee Tank',
            '6': 'Sweatshirt Hoodie',
            '7': 'Jackets Vest',
            '8': 'Shirt Polo',
            '9': 'Suiting',
            '10': 'Blouses Shirts',
            '11': 'Cardigans',
            '12': 'Dresses',
            '13': 'Graphic Tees',
            '14': 'Jackets Coats',
            '15': 'Leggings',
            '16': 'Rompers Jumpsuits',
            '17': 'Skirts',
        }

        for key, value in category_choices.items():
            if category == value:
                category = key

        if request.user.is_authenticated:
            user_id = request.user.id
            has_added = Cart.objects.all().filter(product_id=product_id, user_id=user_id)
            if has_added:
                messages.error(request, 'You have already added to cart for this product check you cart to update')
                return redirect('/products/' + product_id)

        cart = Cart(product_id=product_id, product=product, user_id=user_id, product_price=product_price,
                    quantity=quantity, category=category, photo=photo)

        cart.save()

        messages.success(request, 'Added To Cart')
        return redirect('/products/' + product_id)


def cartcheckout(request):
    if '_update' in request.POST:
        product_id = request.POST['product_id']
        user_id = request.POST['user_id']
        quantity = request.POST['quantity']
        change = Cart.objects.get(product_id=product_id, user_id=user_id)
        change.quantity = quantity
        change.save()

    elif '_remove' in request.POST:
        product_id = request.POST['product_id']
        Cart.objects.filter(product_id=product_id).delete()

    return redirect('cartpage')


def import_data(request):
    cursor = connection.cursor()
    import os
    if os.path.isfile("D:/python/ecommerce/algo/data.csv"):
        os.remove("D:/python/ecommerce/algo/data.csv")

    sql = "COPY (SELECT user_id,category FROM public.carts_cart) TO STDOUT WITH CSV HEADER"
    with open("D:/python/ecommerce/algo/data.csv ", "w") as file:
        cursor.copy_expert(sql, file)

    df = read_csv("D:/python/ecommerce/algo/data.csv")
    df["n"] = 1
    table = df.pivot_table(index=["user_id"], columns=["category"], values="n")
    table = table.fillna(0).reset_index()
    cols = table.columns[1:]
    cluster = KMeans(n_clusters=5)
    table["cluster"] = cluster.fit_predict(table[table.columns[2:]])
    pca = PCA(n_components=5)
    table['x'] = pca.fit_transform(table[cols])[:, 0]
    table['y'] = pca.fit_transform(table[cols])[:, 1]
    table = table.reset_index()
    user_data = table[["user_id", "cluster"]]

    user_data.to_csv("D:/python/ecommerce/algo/user_cluster.csv", index=False)

    cluster_no = int(user_data[(user_data['user_id'] == request.user.id)].iloc[0]['cluster'])
    cluster_no+=1
    #print(cluster_no)
    user = User.objects.get(id=request.user.id)
    group = Group.objects.get(name = "Cluster "+str(cluster_no))
    user.groups.add(group)

    user_id = request.user.id
    print(user_id)

    remove_from_cart = Cart.objects.filter(user_id=user_id)
    for remove_cart in remove_from_cart:
        remove_cart.is_published=False
        remove_cart.save()

    messages.success(request, 'You have purchased the item')
    return redirect('index')
