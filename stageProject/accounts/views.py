from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import Product , Order ,customer
from .forms import OrderForm , CreateUserForm ,CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user , allowed_users , admin_only
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@unauthenticated_user
def registerPage(request):
     form = CreateUserForm()
     if request.method == 'POST' :
          form = CreateUserForm(request.POST) 
          if form.is_valid():
               user = form.save()
               username = form.cleaned_data.get('username')

               messages.success(request, "compte creer pour " + username)
               return redirect('login')
     context = {'form':form}
     return render(request,'accounts/register.html', context) 
@unauthenticated_user
def loginPage(request):
     if request.method == 'POST' :
          username = request.POST.get('username')
          password = request.POST.get('password')

          user = authenticate(request,username=username , password=password)
          if user is not None :
               login(request,user)
               return redirect('home')
          else : 
               messages.info(request, "username or pwd inncorete " ) 
          #return render(request,'accounts/login.html', context) 
     context = {}
     return render(request,'accounts/login.html', context) 
def logoutUser(request):
     logout(request)
     return redirect('login')
@login_required(login_url='login')   
@allowed_users(allowed_roles=['customer']) 
def userPage(request):
     orders = request.user.customer.order_set.all()
     total_orders =  orders.count()
     Delivered = orders.filter(status='Delivered').count()
     Pending = orders.filter(status='Pending').count()
     print('Orders' , orders)
     context = {'orders':orders , 'total_orders':total_orders , 'Delivered':Delivered , 'Pending':Pending}
     return render(request,'accounts/user.html', context) 
@login_required(login_url='login')   
@allowed_users(allowed_roles=['customer','admin']) 
def accountSettings(request):
     customer = request.user.customer
     form = CustomerForm(instance=customer)
     if request.method == 'POST':
        form = CustomerForm(request.POST , request.FILES , instance=customer)
        if form.is_valid():
           form.save()
     context = {'form':form}
     return render(request , 'accounts/account_settings.html' , context)
@login_required(login_url='login')   
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = customer.objects.all()
    total_customers = customers.count()
    total_orders =  orders.count()
    Delivered = orders.filter(status='Delivered').count()
    Pending = orders.filter(status='Pending').count()
    context = {'orders':orders , 'customers':customers , 'total_customers':total_customers , 'total_orders':total_orders , 'Delivered':Delivered , 'Pending':Pending}
    return render(request,'accounts/dashboard.html', context)
@login_required(login_url='login')  
@allowed_users(allowed_roles=['admin','customer'])   
def produit(request):
     products = Product.objects.all()
     return render(request,'accounts/produits.html' , {'products':products})
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])     
def costume(request , pk_test):
     costumer = customer.objects.get(id=pk_test)
     orders = costumer.order_set.all()
     order_count =  orders.count()
     myFilter = OrderFilter(request.GET , queryset=orders)
     orders=myFilter.qs
     context = {'costumer':costumer ,'orders': orders ,'order_count': order_count ,'myFilter': myFilter}
     return render(request,'accounts/costume.html',context)
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin'])    
def createOrder(request,pk):
     OrderFormSet = inlineformset_factory(customer , Order , fields=('product','status'),extra=5)
     costumer = customer.objects.get(id=pk)
     formset = OrderFormSet(queryset=Order.objects.none(), instance=costumer)
    # form = OrderForm(initial={'costumer':costumer})
     if request.method == 'POST' :
          #print('Printing Post',request.POST)
           #form = OrderForm(request.POST)
          formset = OrderFormSet(request.POST , instance=costumer)
          if formset.is_valid():
                formset.save()
                return redirect('/')
     context = {'formset':formset}
     return render(request,'accounts/order_form.html',context)
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin'])    
def updateOrder(request,pk):
     
     order = Order.objects.get(id=pk)
     formset = OrderForm(instance=order)
     if request.method == 'POST' :
          #print('Printing Post',request.POST)
           formset = OrderForm(request.POST,instance=order)
           if formset.is_valid():
                formset.save()
                return redirect('/')
     context = {'formset':formset}
     return render(request,'accounts/order_form.html',context)
@login_required(login_url='login')    
@allowed_users(allowed_roles=['admin']) 
def deleteOrder(request,pk):

     order = Order.objects.get(id=pk)
     if request.method == 'POST' :
               order.delete()
               return redirect('/')
     context = {'item':order}
     return render(request,'accounts/delete.html',context)