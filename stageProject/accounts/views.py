from django.shortcuts import render
from django.http import HttpResponse
from .models import Product , Order ,customer
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

