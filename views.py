from django.shortcuts import render,redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
import razorpay
import json

# Create your views here.
def first(request):
	return render(request,"home.html")

def contact(request):
	return render(request,"contact.html")

def cart(request):
	try:
		carts = request.session['cart_info']
		print("=="*30)
		print(carts)
		request.session['cart_disp_count'] = True
		gross_value=0
		for i in carts:
			for k,v in i.items():
				gross_value+=int(v[-1])*int(v[-2])
		request.session['total_amount']=gross_value
		return render(request,"cart.html",{'allcart':carts})
	except:
		request.session['cart_disp_count']=False
		return render(request,"cart.html")
	#return render(request,"cart.html")

def product(request):
	ob=products.objects.all()
	return render(request,"product.html",{'records':ob})

def single_details(request,iid):
	i_obj=products.objects.get(slug=iid)
	return render(request,"single_details.html",{"i_records":i_obj})

def carts(request):
	btn = request.POST['test']
	qntity=request.POST['qntity']
	uslug=request.POST['slug']
	print(qntity)
	print(uslug)
	i_obj=products.objects.get(slug=uslug)
	print(i_obj)
	
	if(btn == "buy"):
		print("work for buy")
		total = int(qntity)*int(i_obj.pprice)
		request.session['total_amount'] = total
		return redirect('/checkout')
	else:
		print(i_obj.product_image_set.all()[0].image.url)
		single_item={uslug:[i_obj.product_image_set.all()[0].image.url,i_obj.pname,i_obj.pprice,qntity]}
		print("--"*30)
		print(single_item)

		try:
			v=request.session['cart_info']
			f=0
			for x in v:
				if uslug in x:
					h=int(x[uslug][-1])
					h+=int(qntity)

					x[uslug][-1]=str(h)
					f=1

			if f==0:
				v.append(single_item)
			request.session['cart_info']=v
		except Exception as e:
			request.session['cart_info']=[single_item]
		print('details             ',request.session['cart_info'])
		request.session['cart_count']=len(request.session['cart_info'])
	return redirect('/cart')

def remove_cart(request,kslug):
	i=0
	ss=request.session['cart_info']
	for x in ss:
		if kslug in x:
			break
		else:
			i+=1
	ss.pop(i)
	print("---"*30)
	request.session['cart_info']=ss 
	request.session['cart_count']=len(request.session['cart_info'])
	#print(kslug)
	return redirect('/cart')
	
def login(request):
	try:
		if(request.session['error_msg']==2):
			msg1="plzzz enter correct details"
			del request.session['error_msg']
	except:
		msg1=""
	return render(request,"login.html",{'msg1':msg1})

def signup(request):
	try:
		if(request.session['error_msg']==1):
			msg1="plzzz create account"
			del request.session['error_msg']
	except:
		msg1=""
	return render(request,"signup.html",{'msg1':msg1})

def logout(request):
	del request.session['user_details']
	return redirect("/login")

def about(request):
	return render(request,"about_us.html")

def blog(request):
	return render(request,"blog.html")

def blog_details(request):
	return render(request,"blog-details.html")

def testimonial(request):
	return render(request,"testimonial.html")

def terms(request):
	return render(request,"terms.html")

def info(request):
	i = data.objects.all()
	return render(request,"signup.html",{"records":data})

def form(request):
	return render(request,"signup.html")

def value(request):
	a=request.POST['na']
	b=request.POST['ad']
	c=request.POST['em']
	d=request.POST['phn']
	e=request.POST['un']
	f=request.POST['ps']


	ob=data()
	ob.name=a
	ob.address=b
	ob.email=c 
	ob.contact=d 
	ob.username=e 
	ob.password=f 
	ob.save()
	
	return redirect("/login")

def put(request):
	x=request.POST['un']
	y=request.POST['ps']
	print(x)
	print(y)
	try:
		ob=data.objects.get(username=x)
		print(ob)
		if(ob.username==x and ob.password==y):
			arr=[ob.name,ob.address,ob.email,ob.contact,ob.username,ob.password]
			request.session['user_details']=arr
			return redirect('/home')
		else:
			request.session['error_msg']=2
			return redirect('/login')
	except Exception as e:
		request.session['error_msg']=1
		return redirect('/signup')

def payu_checkoutfun(request):
	# razorpay integration
	if request.method == "POST":
		name = request.session['user_details'][1]
		print(name)
		amount = request.session['total_amount']
		print(amount)
		client = razorpay.Client(auth=('rzp_test_TeZssD8bfY472F', '0GOce3YYyIPhF3Hamaremjdw'))
		razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
            )
		print(razorpay_order)
		order = Order.objects.create(
        	name=name, amount=amount, provider_order_id=razorpay_order["id"]
        	)
		print(order)
		order.save()
		return render(
			request,
			"payment.html",
			{
				# "callback_url": "http://" + "127.0.0.1:8000" + "/callback/", 
				"callback_url": "http://localhost:8000/callback",
				"razorpay_key": 'rzp_test_TeZssD8bfY472F',
				"order": order,
			},
		)
	return render(request, "payment.html")

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=('rzp_test_TeZssD8bfY472F', '0GOce3YYyIPhF3Hamaremjdw'))
        return client.utility.verify_payment_signature(response_data)

    print("Request POST data:", request.POST)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        print(payment_id)
        provider_order_id = request.POST.get("razorpay_order_id", "")
        print(provider_order_id)
        signature_id = request.POST.get("razorpay_signature", "")
        print(signature_id)
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
        else:
            order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})