from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    date_ajout = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return self.name


class Produit(models.Model):
    title = models.CharField(max_length=200)
    prix = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='categorie', on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return self.title

class customer(models.Model):
    user = models.OneToOneField(User , null=True , on_delete=models.CASCADE)
    name = models.CharField(max_length=200 , null=True)
    phone = models.CharField(max_length=200 , null=True)
    email = models.CharField(max_length=200 , null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=200 , null=True)
  
    def __str__(self):
        return self.name
       
class Product(models.Model):
    CATEGORY =(
        ('indoor','indoor') ,
        ('Outdoor','Outdoor') , 
        )
     
    name = models.CharField(max_length=200 , null=True)
    price = models.FloatField(null=True)
    Category = models.CharField(max_length=200 , null=True , choices=CATEGORY)
    description = models.CharField(max_length=200 , null=True , blank=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True) 
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.name

    
class Order(models.Model):
    STATUS =(
        ('Pending','Pending') ,
        ('Out for delivery','Out for delivery') , 
        ('Delivered','Delivered') , 
    )
    Costumer = models.ForeignKey(customer,null=True,on_delete=models.SET_NULL)
    product  = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True , null=True)  
    status = models.CharField(max_length=200 , null=True , choices=STATUS)
    note = models.CharField(max_length=1000 , null=True )
    def __str__(self):
        return self.product.name