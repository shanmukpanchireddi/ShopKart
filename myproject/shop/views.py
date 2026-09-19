from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from shop.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json
# Create your views here.
def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json # only needed if you don't include {% csrf_token %} in the template
def favview(request):
    if request.user.is_authenticated:
        fav=Fav.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})
    else:
        return redirect("/")
def fav(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Fav.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Fav.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
def addtocart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_qty = int(data.get('product_qty', 0))
                product_id = int(data.get('pid'))

                # Fetch product
                product_check = Product.objects.get(id=product_id)

                if product_check:
                    # Check if item already in cart
                    if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                        return JsonResponse({'status': "Product already in cart!"}, status=200)
                    else:
                        if product_check.quantity >= product_qty:
                            Cart.objects.create(
                                user=request.user,
                                product=product_check,
                                product_qty=product_qty
                            )
                            return JsonResponse({'status': "Product added to cart!"}, status=200)
                        else:
                            return JsonResponse({'status': "Only limited stock available!"}, status=200)

            except Product.DoesNotExist:
                return JsonResponse({'status': "No such product found!"}, status=404)
            except Exception as e:
                return JsonResponse({'status': f"Something went wrong: {str(e)}"}, status=500)

        else:
            return JsonResponse({'status': "Login to add items to cart"}, status=401)
    else:
        return JsonResponse({'status': "Invalid access!"}, status=400)
def cart(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect("/")
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    messages.success(request, "Item removed from cart 🛒❌")
    return redirect("/cart")
def remove_fav(request,fid):
    item=Fav.objects.get(id=fid)
    item.delete()
    messages.success(request, "Item removed from cart ❤️‍🔥❌")
    return redirect("/favview")

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                return redirect("/")
            else:
                messages.error(request,"Invalid UserName or Password 🙄")
                return redirect('login')
    return render(request,'shop/login.html')
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "LogOut SuccessFull 😶‍🌫️")
    return redirect('login')

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Successfull Please Continue Login ☺️")
            return redirect('login')
    return render(request,"shop/register.html",{'form':form})
def collections(request):
    catog=Catog.objects.filter(status=0)
    return render(request,"shop/collections.html",{"catog":catog})
def collectionsview(request,name):
    if(Catog.objects.filter(name=name,status=0)):
        products=Product.objects.filter(catof__name=name)
        return render(request,"shop/products/index.html",{"products":products,"catog_name":name})
    else:
        messages.warning(request,"No such Catagory Found")
        return redirect('collections')
    

def product_details(request,cname,pname):
    if(Catog.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_page.html",{"products":products})
        else:
            messages.warning(request,"No such Catagory Found")
            return redirect('collections')


    else:
        messages.warning(request,"No such Catagory Found")
        return redirect('collections')
