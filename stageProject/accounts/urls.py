from django.urls import path
from . import views
urlpatterns = [
    path('', views.home , name='home'),
    path('produit/', views.produit , name='produit'),
    path('costume/<str:pk_test>/', views.costume , name='costume'),
    
]