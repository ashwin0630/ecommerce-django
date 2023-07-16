from django.shortcuts import render,redirect,HttpResponse
from shop.form import customuserform,sellerform
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_protect
# Create your views here.
@csrf_protect
def home(request):
    products=product.objects.filter(trending=1)
    return render(request,"index.html",{"products":products})

@csrf_protect
def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            product_status=product.objects.get(id=product_id)
            if product_status:
                if cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        cart.objects.create(user=request.user,product_id=product_id,product_quantity=product_qty)
                        return JsonResponse({'status':'product added to cart'}, status=200)
                    else:
                        return JsonResponse({'status':'product stock not available'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'}, status=200)
    
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

@csrf_protect
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"logout successful")
        return redirect("/")


@csrf_protect
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=="POST":
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Registration successful you can login now")
                return redirect("/")
            else:
                messages.error(request,"invalid username or password")
                return redirect("login")    
        return render(request,"login.html")

@csrf_protect
def register(request):
    form=customuserform()
    if request.method=="POST":
        form=customuserform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration successful you can login now")
            return redirect('/login')
    return render(request,"register.html",{'form':form})

@csrf_protect
def collections(request):
    Catagory=catagory.objects.filter(status=0)
    return render(request,"collections.html",{"Catagory":Catagory})

@csrf_protect
def collectionsview(request,name):
    if catagory.objects.filter(name=name,status=0):
        products=product.objects.filter(catagory__name=name)
        return render(request,"shop/products/index.html",{"products":products,"cname":name})
    else:
        messages.warning(request,"no such catagory found")
        return redirect("collections")

@csrf_protect
def product_details(request,c_name,p_name):
    if(catagory.objects.filter(name=c_name,status=0)):
        if(product.objects.filter(name=p_name,status=0)):
            products=product.objects.filter(name=p_name,status=0).first()
            return render(request,"shop/products/product_details.html",{"products":products})
        else:
            messages.warning(request,"product not found")
            return redirect("collections")


    else:
        messages.warning(request,"product not found")
        return redirect("collections")
    
@csrf_protect
def cart_page(request):

    if request.user.is_authenticated:
        Cart=cart.objects.filter(user=request.user)
        return render(request,"cart.html",{"cart":Cart})
    else:
        return redirect("/")
    
@csrf_protect
def remove_cart(request,cid):
    cartitem=cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

@csrf_protect
def premium(request):
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=sellerform(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                
        else:
            form=sellerform()
        return render(request,'premium.html',{"form":form})
    else:
        return redirect("/login")






    

