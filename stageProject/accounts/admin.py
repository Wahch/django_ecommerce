from django.contrib import admin

# Register your models here.
from .models import Category, Produit , customer , Product , Order , Tag


# Register your models here.
class AdminCategorie(admin.ModelAdmin):
    list_display = ('name' ,'date_ajout')

class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'prix', 'category', 'date_ajout')


admin.site.register(Produit, AdminProduct)
admin.site.register(Category, AdminCategorie)
admin.site.register(customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)