from cgi import print_form
import email
from logging import exception
from re import A, template
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from store.device_functions import check_finger_return_id

from store.forms import userform
from .models import *
from .forms import *
import serial
import time


def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store.html', context)


def product(request, pk):

    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        # Get user account information
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(
            order=order, product=product)
        orderItem.quantity = request.POST['quantity']
        orderItem.save()

        return redirect('cart')

    context = {'product': product}
    return render(request, 'product.html', context)


def cart(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    context = {'order': order}
    return render(request, 'cart.html', context)


def recharge(request):
    if request.POST:
        fingid = 1
        numb = request.POST['numb']
        print(numb)

        c = Customer.objects.get(id=fingid)

        c.amount = c.amount + int(numb)
        c.save()

        return redirect(auth_recharge)

    return render(request, 'recharge.html')


def delete_event(request, pk):
    ord = OrderItem.objects.get(id=pk)
    ord.delete()
    return redirect('cart')


def checkout(request):
    return render(request, "checkout.html")


def detail(request):
    fingid = check_finger_return_id('c')

    # TODO:All the error cases from the function and the associated error pages
    switcher = {
        -1: HttpResponse("User not found"),
        -2: HttpResponse("Device not found"),
        -3: HttpResponse("Device busy"),
        -4: HttpResponse("Timeout")
    }

    if(int(fingid) < 0):
        return switcher.get(fingid, HttpResponse("Error"))

    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    cust = Customer.objects.get(id=fingid)

    if(cust.amount - order.get_cart_total < 0):
        # TODO: This condition
        return HttpResponse("Insufficient balance. Recharge your wallet")

    cust.amount = cust.amount - order.get_cart_total
    cust.save()

    cart_total = order.get_cart_total
    order.delete()

    context = {'cust': cust, 'cart_total': cart_total}

    return render(request, "detail.html", context)
    # return HttpResponse('Figerprint Match Found. ID: '+id)


def detail_recharge(request):
    return render(request, 'detail_recharge.html')


def auth_recharge(request):

    return render(request, 'auth_recharge.html')


def auth_register(request):
    return render(request, 'auth_register.html')


def reciept(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    context = {'order': order}
    return render(request, 'reciept.html', context)


def register(request):
    if request.POST:
        fingid = 1
        name = request.POST['name']
        email = request.POST['email']
        print(name, email)

        c = Customer.objects.get(id=fingid)
        c.name = name
        c.email = email
        c.save()

        return redirect(auth_register)
    return render(request, 'register.html')
