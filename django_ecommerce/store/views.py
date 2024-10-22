from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    carousel_items = [
        {'image_filename': 'product1.jpg', 'title': 'Product 1'},
        {'image_filename': 'product2.jpg', 'title': 'Product 2'},
        {'image_filename': 'product3.jpg', 'title': 'Product 3'},
    ]
    
    products = [
        {'image_filename': 'product7.jpg', 'title': 'Most Loved Watches'},
        {'image_filename': 'product8.jpg', 'title': 'Shop for your Home Essentials'},
        {'image_filename': 'product9.jpg', 'title': 'New Home Arrivals'},
        {'image_filename': 'product10.jpg', 'title': 'Top Categories in Kitchen'},
        {'image_filename': 'product11.jpg', 'title': 'Refresh your Space'},
        {'image_filename': 'product12.jpg', 'title': 'Most Loved Travel Essentials'},
    ]
    
    context = {
        'carousel_items': carousel_items,
        'products': products,
    }
    
    return render(request, 'store/home.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def contact_us(request):
    return render(request, 'store/contact_us.html')

def about_us(request):
    return render(request, 'store/about_us.html')
