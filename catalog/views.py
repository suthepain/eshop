from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from . import handlers

# Create your views here.
def main_page(request):
    all_categories = models.Category.objects.all()
    all_products = models.Product.objects.all()

    # poluchit peremennuyu iz front chasti, yesli ono yest
    search_value_from_front = request.GET.get('pr')

    if search_value_from_front:
        all_products = models.Product.objects.filter(name__contains=search_value_from_front)
    # peredacha peremennix iz beka na front
    context = {'all_categories':all_categories, 'all_products':all_products}
    # pokaz kontenta iz html fayla
    return render(request, 'index.html', context)

# poluchit produkti iz konkretnoy kategorii
def get_category_products(request, pk):
    # poluchit vse tovari iz konkretnoy kategorii
    exact_category_products = models.Product.objects.filter(category_name__id=pk)

    # peredacha peremennix iz beka na front
    context = {'category_products': exact_category_products}

    # ukazat html
    return render(request, 'category.html', context)

# funktsiya polucheniya opredelennogo produkta
def get_exact_product(request, name, pk):
    # nahodim produkt iz bazi
    exact_product = models.Product.objects.get(name=name, id=pk)

    # peredacha dannih iz beka na front
    context = {'product': exact_product}

    return render(request, 'product.html', context)

# Funktsiya dobavleniya produkta v korzinu
def add_pr_to_cart(request, pk):
    # Poluchit vibrannoe kolichestva produkta iz front chasti
    quantity = request.POST.get('pr_count')

    # Nahodim sam product
    product_to_add = models.Product.objects.get(id=pk)
    # Dobavlenie dannih
    models.UserCart.objects.create(user_id=request.user.id, user_product=product_to_add, user_product_quantity=quantity)

    return redirect('/')

# Poluchit korzinu polzovatelya
def user_cart(request):
    products = models.UserCart.objects.filter(user_id=request.user.id)
    context = {'cart_products': products}
    return render(request, 'user_cart.html', context)

# oformlenie zakaza

def complete_order(request):
    # Poluchayem korzinu polzovatelya
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)
    if request.method == 'POST':
        result_message = 'Новый заказ(из Сайта)\n\n'
    # счетчик для подсчета итога для корзины
    total_for_all_cart = 0
    for cart in user_cart:
        result_message +=f'Название товара: {cart.user_product}\n' \
                         f'Количество: {cart.user_product_quantity}'
    handlers.bot.send_message(-669247380, result_message)
    user_cart.delete()
    return redirect('/')
    return render(request, 'user_cart.html', {'user_cart': user_cart})
def delete_from_user_cart(request, pk):
    user_cart = models.UserCart.objects.filter(user_id=request.user.id, user_product=pk)
    user_cart.delete()
    return redirect('/cart')