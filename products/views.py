from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def new(request):
    return HttpResponse('New Products')

def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('id')
        product = Product.objects.get(id=product_id)

        cart = request.session.get('cart', [])
        
        # Check if product is already in the cart
        found = False
        for item in cart:
            if item['id'] == product.id:
                item['quantity'] += 1  # Increase quantity
                found = True
                break
        
        if not found:
            cart.append({'id': product.id, 'name': product.name, 'price': product.price, 'image_url': product.image_url, 'quantity': 1})
        
        request.session['cart'] = cart
        request.session.modified = True

        return redirect('product_list')

from django.http import JsonResponse
import logging

# Get the logger
logger = logging.getLogger(__name__)

def remove_from_cart(request, product_id):
    try:
        # Retrieve the cart from the session
        cart = request.session.get('cart', [])

        # Log the cart before modification
        logger.debug("Cart before removal: %s", cart)

        # Find the product in the cart by matching the product_id
        for item in cart:
            if item['id'] == product_id:
                # Ensure the item has a 'quantity' key, if not, set it to 1
                if 'quantity' not in item:
                    item['quantity'] = 1
                
                # Check if the quantity is greater than 1, then decrement it
                if item['quantity'] > 1:
                    item['quantity'] -= 1
                else:
                    # If quantity is 1, remove the item from the cart entirely
                    cart.remove(item)
                break  # Exit the loop once the item is found and removed

        # Save the updated cart back into the session
        request.session['cart'] = cart
        request.session.modified = True

        # Log the cart after modification
        logger.debug("Cart after removal: %s", cart)

        # Return a JSON response indicating the item was removed and providing the updated cart count
        return redirect("/cart")
    
    except Exception as e:
        # Log the error
        logger.error("Error removing item from cart: %s", str(e))
        return JsonResponse({'message': 'An error occurred while removing the item from the cart.'}, status=500)

def get_cart_total(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return JsonResponse({'cart_total': round(total, 2)})

def get_cart_count(request):
    cart = request.session.get('cart', [])
    return JsonResponse({'cart_count': len(cart)})

def view_cart(request):
    """Displays the cart page."""
    cart = request.session.get('cart', [])
    return render(request, 'cart.html', {'cart': cart})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("product_list")
        else:
            messages.success(request, ("An Error occurred, Please Retry Login"))
            return redirect("login")
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    return redirect("product_list")