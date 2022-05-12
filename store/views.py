from django.shortcuts import render, redirect
from django.http import HttpResponse

from store.forms import userform
from .models import *
from .forms import *
import serial
import time

def store(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'store.html', context)

def product(request, pk):
	product = Product.objects.get(id=pk)

	if request.method == 'POST':
		product = Product.objects.get(id=pk)
		#Get user account information
		try:
			customer = request.user.customer	
		except:
			device = request.COOKIES['device']
			customer, created = Customer.objects.get_or_create(device=device)

		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
		orderItem.quantity=request.POST['quantity']
		orderItem.save()

		return redirect('cart')

	context = {'product':product}
	return render(request, 'product.html', context)

def cart(request):
	try:
		customer = request.user.customer
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device=device)

	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	context = {'order':order}
	return render(request, 'cart.html', context)

def recharge(request):
	# ser = serial.Serial()
	# ser.baudrate = 19200 
	# ser.port = 'COM3'
	# print(ser)
	return render(request, 'recharge.html')

def delete_event(request, pk):
	ord = OrderItem.objects.get(id=pk)
	ord.delete()
	return redirect('cart')

def register(request):
    if request.method == 'POST':
        a=userform(request.POST)
        if a.is_valid():
            name=a.cleaned_data['name']
            email=a.cleaned_data['email']
           
            b=Customer(name=name,email=email)
            b.save()
            return redirect(store)
        else:
            return HttpResponse('registration incomplte')
    else:
        return render(request,'register.html')

def checkout(request):
		print("Check fingerprint")
		import serial.tools.list_ports

		currentPort = None

		ports = list(serial.tools.list_ports.comports())
		# print("port port is", ports[0])
		for p in ports:
			print(p.description)
			if "CP210x" in p.description:
				currentPort = p
				break

		if currentPort == None:
			print("No device found")
			return
		print("port is", currentPort.device)

		arduino = serial.Serial(port=currentPort.device,
								baudrate=9600, timeout=.1)

		arduino.write(bytes('c', 'utf-8'))
		arduino.reset_input_buffer()

		while(not arduino.in_waiting):
			print("waiting...")
			time.sleep(0.5)

		fingid = arduino.readline().decode('utf-8')
		print('The detected ID is ', id)
		arduino.write(bytes('x', 'utf-8'))

		cust = Customer.objects.get(id=fingid)
		return HttpResponse('name is' +cust.name)	
		# return render(request, "checkout.html")
		# return HttpResponse('Figerprint Match Found. ID: '+id)

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

	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	context = {'order':order}
	return render(request, 'reciept.html', context)

    	