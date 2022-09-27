from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.views.generic.base import TemplateView,RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
import urllib
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulStoneSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def loginUser(request):
    '''Function to login a user'''
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
         
        try:
            user = User.objects.get(username=username, password=password)
        except:
            print('Invalid credentials')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('Invalid credentials')
    context = {'page': page}
    return render(request, 'store/login_register.html',context)
        
def logoutUser(request):
    '''Function to log out a user'''
    logout(request)
    return redirect('login') 

def registerUser(request):
    '''Function to register a user'''
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('login')

        else:
            messages.success(
                request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'store/login_register.html', context)

class Home(ListView):
    '''A class-based list view that displays a list of products on the homepage'''
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'product'

def products(request, pk):
    '''Function to get a product and render it to the template'''
    if request.user.is_authenticated:
        product = Product.objects.get(pk = pk)
        tag = product.tags.values_list('name', flat=True)
        if tag.first():
            context = {'product': product, 'tag': tag[0]+'⭐'}
        else:
            tag = ''
            context = {'product': product, 'tag': tag}
                
        return render(request, 'store/product.html', context) 
    else:
        return redirect('login')

def checkout(request):
    '''Function that is called when the product is checkout. Returns the checkout information if user is logged in'''
    if request.user.is_authenticated:  
        buyer = request.user.buyer
        order, created = Cart.objects.get_or_create(buyer = buyer, complete = False)
        items = order.cartitem_set.all() 
        context = {'items': items, 'cart':order}
        return render(request, 'store/checkout.html',context)
            
    else:
        return redirect('login')
    
def checkout2(request, pk):
    '''Function that is called when the product is checkout. Returns the checkout information if user is logged in'''
    if request.user.is_authenticated:  
        buyer = request.user.buyer
        item = Product.objects.get(id = pk)
        order, created = Cart.objects.get_or_create(buyer = buyer, complete = False)
        product, created = CartItem.objects.get_or_create(product__pk=pk, order = order, product = item)   
        product.quantity = product.quantity + 1   
        product.save()
        items = order.cartitem_set.all() 
        context = {'items': items, 'cart':order}
        return render(request, 'store/checkout.html',context)
            
    else:
        return redirect('login')
# @login_required
def cart(request):
    '''Function to display cart items and information'''
    if request.user.is_authenticated:
        buyer = request.user.buyer
        order, created = Cart.objects.get_or_create(buyer = buyer, complete = False)
        items = order.cartitem_set.all() 
        context = {'items': items, 'cart':order}
        return render(request, 'store/cart.html', context) 
    else:
        return redirect('login')
        
def cart2(request, pk):
    '''Function that increases cart items count and returns a list of cart items'''
    if request.user.is_authenticated:
        cart_checkout(request, pk)
        return redirect('home')
    else:
       return redirect('login')
   
def cart3(request, pk):
    '''Function that increases cart items count and returns a list of cart items'''
    if request.user.is_authenticated:
        cart_checkout(request, pk)
        return redirect('cart')
    else:
        return redirect('login')
    
def add(request, pk):
    '''Function that increases cart items count when clicked on add image and returns a list of cart items'''
    if request.user.is_authenticated:
        product = CartItem.objects.get(product__pk=pk, ) 
        stock = Product.objects.get(id = pk)  
        product.quantity = product.quantity + 1   
        if product.quantity >= stock.stock:
            product.quantity = stock.stock 
            messages.warning(request, "Out of stock")  
        product.save()  
        return redirect('cart')
    else:
        return redirect('login')
        
def sub(request, pk):
    '''Function that decreases cart items count when clicked on add image and returns a list of cart items'''
    if request.user.is_authenticated:
        product = CartItem.objects.get(product__pk=pk)   
        product.quantity = product.quantity - 1 
        if product.quantity <= 0:
            product.quantity = 0 
            product.delete()
            messages.error(request, 'Item removed from cart')
        else:    
            product.save()  
        return redirect('cart')
    else:
        return redirect('login') 
        
def seller(request):
    '''Function to display all sellers and their information'''
    tag = []
    sellers = Seller.objects.all()
    for seller in sellers:
        tag.append(seller.product_set.values_list('id',flat = True)) 
    context = {'sellers': sellers, 'id': tag}
    return render(request, 'store/seller.html', context)

def delete_item(request, pk):
    '''Function to remove an item from the cart'''
    item = CartItem.objects.get(product__pk = pk)
    if request.method == 'GET':
        item.delete()
        return redirect('cart')
    context = { 'item': item }
    return render(request, 'store/cart.html', context) 

def cart_checkout(request, pk):
    '''Helper function'''
    buyer = request.user.buyer
    item = Product.objects.get(id = pk)
    order, created = Cart.objects.get_or_create(buyer = buyer, complete = False)
    product, created = CartItem.objects.get_or_create(product__pk=pk, order = order, product = item)   
    product.quantity = product.quantity + 1   
    product.save()
    

    
    
