from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('products/',views.products, name='products'),
    path('customer/<str:pk>/',views.customer, name='customer'),
    path('forms/<str:pk>/',views.createorder,name='forms'),
    path("update/<str:pk_update>", views.updateorder, name="update"),
    path('delete/<str:pk_delete>', views.deleteorder, name='delete'),

]