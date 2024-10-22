from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('contact/', views.contact_us, name='contact_us'),
    path('about/', views.about_us, name='about_us'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
