from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import SimpleLazyObject, LazyObject

from .models import Plat, Cart, Order, DeliveryPrice, Category


def index(request):
    plats = Plat.objects.all()
    categories = Category.objects.all()
    search_input = request.GET.get('search-bar')
    if search_input != "" and search_input is not None:
        plats = Plat.objects.filter(name__icontains=search_input)
    return render(request, 'store/index.html', {"plats": plats, 'categories': categories})


def plat_detail(request, id):
    plat = get_object_or_404(Plat, id=id)
    plats = Plat.objects.all()
    categories = Category.objects.all()
    return render(request, 'store/plat_detail.html', {'plat': plat, "plats": plats, 'categories': categories})


def create_cart_and_order(request, id):
    user = request.user
    plat = get_object_or_404(Plat, id=id)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, plat=plat)
    if created:
        cart.orders.add(order)
        cart.save
    else:
        order.quantity += 1
        order.save()


# def add_to_cart_from_menu(request, id):
#     create_cart_and_order(request, id)
#     # return redirect(reverse('index', kwargs={'slug': slug}))
#     return redirect(reverse('index'))
#
#
# def add_to_cart_from_more_details(request, id):
#     create_cart_and_order(request, id)
#     return redirect(reverse('plat', kwargs={'id': id}))


def add_to_cart(request):
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user)

    if request.POST.get('action') == 'post':
        plat_id = int(request.POST.get('plat_id'))
        plat = get_object_or_404(Plat, id=plat_id)
        order, created = Order.objects.get_or_create(user=user, plat=plat)
        if created:
            cart.orders.add(order)
            cart.save
        else:
            order.quantity += 1
            order.save()
        response = JsonResponse({'cart_total_orders': str(cart.orders.count())})
        return response


# def force_evaluate_lazy_object(obj):
#     if isinstance(obj, SimpleLazyObject) or isinstance(obj, LazyObject):
#         return obj._wrapped
#     return obj

def get_cart(request):
    user = request.user
    if user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    return 'no user - no cart'


def calculate_shopping_balance(request):
    cart = get_cart(request)
    orders = cart.orders.all()
    shopping_balance = 0
    for order in orders:
        shopping_balance += order.calculate_balance()
    return shopping_balance


def go_to_cart(request):
    cart = get_cart(request)
    if cart == 'no user - no cart':
        return HttpResponse('User disconnected. Please go back to home page')
    orders = cart.orders.all()
    delivery_price = DeliveryPrice.objects.all()
    cart_balance = calculate_shopping_balance(request)
    # cart.total_amount = 500

    return render(request, 'store/cart.html', {'orders': orders, 'cart_balance': cart_balance, 'delivery_price': delivery_price[0]})


def get_cart_order(request, plat_id, cart):
    plat = get_object_or_404(Plat, id=plat_id)
    order = cart.orders.all().get(plat=plat)
    return order


def delete_order(request):
    if request.POST.get('action') == 'post':
        if cart := request.user.cart:
            plat_id = int(request.POST.get('plat_id'))
            order = get_cart_order(request, plat_id, cart)
            cart.orders.remove(order)
            order.delete()
            delivery_price = DeliveryPrice.objects.all()[0]
            shopping_balance = calculate_shopping_balance(request)
            response = JsonResponse({'id': plat_id, 'shopping_balance': shopping_balance, 'delivery_price': delivery_price.price, 'cart_items_number': cart.orders.count()})
            return response


def modify_order(request):
    cart = request.user.cart
    if request.POST.get('action') == 'post':
        order_qty = request.POST.get('order_qty')
        plat_id = request.POST.get('plat_id')
        _list = plat_id.split(sep='-')
        plat_id = int(_list[-1])
        order = get_cart_order(request, plat_id, cart)
        order.quantity = int(order_qty)
        order.save()
        cart.save()
        order_price = order.calculate_balance()
        shopping_balance = calculate_shopping_balance(request)
        response = JsonResponse({'qty': order_qty, 'order_price': order_price, 'shopping_balance': shopping_balance})
        return response


def pay_for_shopping(request):
    return HttpResponse('Sorry our site is currently undergoing maintenance.<br>Please come back later.')

