from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.http import JsonResponse
import json
import datetime
# Create your views here.
from . models import *

from . utils import cookieCart, cartData, guestOrder


def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    plist = Category.objects.all()
    pproduct = Product.objects.all()
    context = {'plist': plist, 'pproduct': pproduct, 'cartItems': cartItems}
    return render(request, 'Store/index.html', context)


def productList(request, slug):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.filter(cat__category=slug)
    context = {'products': products, 'cartItems': cartItems, 'header': slug}
    return render(request, 'Store/product-list.html', context)
    # return HttpResponse("Product List for " + slug + str(products))


class ProductDetails(DetailView):

    template_name = 'Store/product_detail.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductDetails, self).get_context_data(**kwargs)
        data = cartData(self.request)
        cartItems = data['cartItems']
        context['cartItems'] = cartItems
        return context


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'Store/view-cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        cadd = UserAdderess.objects.filter(user=request.user)
    else:
        cadd = ""

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'cadd': cadd}

    return render(request, 'Store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    # test on cmd teminal
    print('action: ', action)
    print('ProductId: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Itme was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True

    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
    )

    return JsonResponse('Payment Complete!', safe=False)
