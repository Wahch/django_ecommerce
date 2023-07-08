from django.urls import path
from . import views
urlpatterns = [
    path('', views.home , name='home'),
    path('produit/', views.produit , name='produit'),
    path('costume/<str:pk_test>/', views.costume , name='costume'),
    path('create_order/<str:pk>/', views.createOrder , name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder , name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder , name='delete_order'),
]