from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import Product , Order ,customer
from .forms import OrderForm
# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = customer.objects.all()
    total_customers = customers.count()
    total_orders =  orders.count()
    Delivered = orders.filter(status='Delivered').count()
    Pending = orders.filter(status='Pending').count()
    context = {'orders':orders , 'customers':customers , 'total_customers':total_customers , 'total_orders':total_orders , 'Delivered':Delivered , 'Pending':Pending}
    return render(request,'accounts/dashboard.html', context)
def produit(request):
     products = Product.objects.all()
     return render(request,'accounts/produits.html' , {'products':products})
def costume(request , pk_test):
     costumer = customer.objects.get(id=pk_test)
     orders = costumer.order_set.all()
     order_count =  orders.count()
     context = {'costumer':costumer ,'orders': orders ,'order_count': order_count}
     return render(request,'accounts/costume.html',context)
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
def updateOrder(request,pk):
     
     order = Order.objects.get(id=pk)
     form = OrderForm(instance=order)
     if request.method == 'POST' :
          #print('Printing Post',request.POST)
           form = OrderForm(request.POST,instance=order)
           if form.is_valid():
                form.save()
                return redirect('/')
     context = {'form':form}
     return render(request,'accounts/order_form.html',context)
def deleteOrder(request,pk):

     order = Order.objects.get(id=pk)
     if request.method == 'POST' :
               order.delete()
               return redirect('/')
     context = {'item':order}
     return render(request,'accounts/delete.html',context)