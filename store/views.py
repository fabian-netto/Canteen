from cgi import print_form
import email
from logging import exception
from re import A, template
import re
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from store.device_functions import check_finger_return_id, enroll_finger_with_id

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
        global numb

        numb = request.POST['numb']
        print(numb)

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
        -1: redirect(user_not),
        -2: redirect(device_not),
        -3: redirect(device_busy),
        -4: redirect(timeout)
    }

    if(fingid < 0):
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
        return redirect(insuff_bal)

    cust.amount = cust.amount - order.get_cart_total
    cust.save()

    cart_total = order.get_cart_total

    context = {'cust': cust, 'cart_total': cart_total}

    return render(request, "detail.html", context)
    # return HttpResponse('Figerprint Match Found. ID: '+id)


def detail_recharge(request):
    if request.POST:
        return redirect('store')
    cust = Customer.objects.get(id=rechargeFingId)
    context = {'cust': cust, 'numb': numb}
    return render(request, 'detail_recharge.html', context)


def auth_recharge(request):
    return render(request, 'auth_recharge.html')


def payment(request):
    fingid = check_finger_return_id('c')
    # TODO:All the error cases from the function and the associated error pages
    switcher = {
        -1: redirect(user_not),
        -2: redirect(device_not),
        -3: redirect(device_busy),
        -4: redirect(recharge_timeout)
    }

    if(int(fingid) < 0):
        return switcher.get(fingid, HttpResponse("Error"))

    global rechargeFingId
    rechargeFingId = fingid

    c = Customer.objects.get(id=fingid)

    c.amount = c.amount + int(numb)
    c.save()
    return render(request, 'payment.html')


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

    if request.POST:
        order.delete()
        return redirect('store')

    context = {'order': order}
    return render(request, 'reciept.html', context)


def register(request):
    if request.POST:
        fingid = 1
        global name
        global email

        name = request.POST['name']
        email = request.POST['email']
        print(name, email)

        return redirect(auth_register)
    return render(request, 'register.html')


def user_not(request):
    return render(request, 'user_not.html')


def device_not(request):
    return render(request, 'device_not.html')


def device_busy(request):
    return render(request, 'device_busy.html')


def timeout(request):
    return render(request, 'timeout.html')


def recharge_timeout(request):
    return render(request, 'recharge_timeout.html')


def register_timeout(request):
    return render(request, 'register_timeout.html')


def insuff_bal(request):
    return render(request, 'insuff_bal.html')


def registration_success(request):
    if request.POST:
        return redirect('store')

    latestId = Customer.objects.latest('id').id
    fingId = latestId+1

    global name
    global email

    success = enroll_finger_with_id(fingId)

    switcher = {
        -1: redirect(user_not),
        -2: redirect(device_not),
        -3: redirect(device_busy),
        -4: redirect(register_timeout)
    }

    if(success < 0):
        return switcher.get(success, HttpResponse("Error"))

    print(str(success) + "<-success")

    if(success == 1):
        print("success is"+str(success) + name + email)
        c = Customer(name=name, email=email, amount=0, id=fingId)
        c.save()

    context = {"cust": c}

    return render(request, 'registration_successful.html', context)
