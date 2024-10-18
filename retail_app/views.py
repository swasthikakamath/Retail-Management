from django.shortcuts import render ,  get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , logout , authenticate
from .models import CustomUserCreationForm 
from django.utils import timezone
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .forms import *
from .models import *
import tensorflow as tf
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from datetime import datetime,timedelta
from django.http import JsonResponse
import numpy as np
from django.core.mail import send_mail
import pandas as pd
from django.db.models import Sum
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, LayerNormalization, Add, MultiHeadAttention, GlobalAveragePooling1D
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential
import optparse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
# Create your views here.
# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
           
#             first_name = form.cleaned_data.get('first_name')
#             last_name = form.cleaned_data.get('last_name')
#             email = form.cleaned_data.get('email')
#             messages.success(request, f'Account created for {first_name}!')
#             return redirect('login_view')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, 'You have been logged in successfully!')
#             return redirect('home')  
#         else:
#             messages.error(request, 'Invalid username or password.')
#     return render(request, 'login.html')
@login_required
def view_sales(request):
    customer = get_object_or_404(Customer, user=request.user)
    print(customer)
    sales = Purchase.objects.filter(customer_id=customer.id).order_by('purchase_date')
    print(sales)
    return render(request, 'sales.html', {'sales': sales})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # 'owner' or 'customer'

        # Debugging role and form input
        print(f"Username: {username}, Role: {role}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the login attempt
            LoginAttempt.objects.create(user=user, login_time=timezone.now())

            if role == 'owner' and hasattr(user, 'profile') and user.profile.role == 'owner':
                login(request, user)
                return redirect('owner_dashboard')
            elif role == 'customer' and hasattr(user, 'profile') and user.profile.role == 'customer':
                login(request, user)
                return redirect('customer_dashboard')
            else:
                messages.error(request, 'Invalid role for user.')
                print(f"Invalid role: {role}, Profile role: {user.profile.role}")

        else:
            messages.error(request, 'Invalid username or password.')
            print(f"Failed login attempt for {username}")

    return render(request, 'login.html')

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This is where the new user is created
            messages.success(request, f'Account created for {user.first_name}! redirecting to customer dashboard')
            login(request, user)
            return redirect('customer_dashboard')
        else:
            # Add this to see what errors are happening
            print(form.errors)  # This will print the form validation errors in your console
            messages.error(request, "There was an error with your submission.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
def logout_view(request):
    logout(request)
    print("User logged out.")
    return redirect('login')  

def home(request):
    return render(request, 'home.html')

@login_required
def customer_dashboard(request):
    if request.user.profile.role != 'customer':
        return redirect('owner_dashboard')
    # Show only available products
    return render(request, 'customer_dashboard.html')

@login_required
def owner_dashboard(request):
    if request.user.profile.role != 'owner':
        return redirect('customer_dashboard')

    # Handle adding a new product
    if request.method == "POST" and 'name' in request.POST:
        form = ProductForm(request.POST, request.FILES)  # Add request.FILES
        if form.is_valid():
            form.save()
        else:
            print(form.errors)  

    # Fetch products to display in the table
    products = Product.objects.all()
   
    context = {
        'products': products,
       
    }
    return render(request, 'owner_dashboard.html', context)

# @login_required
# def update_product(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == "POST":
#         form = ProductForm(request.POST, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('owner_dashboard')  # Redirect back to dashboard after saving
#     return render(request, 'owner_dashboard.html', {'product': product})


# Updated update_product view
@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" has been updated successfully.')
            return redirect('owner_dashboard')
        else:
            messages.error(request, "There was an error updating the product. Please check the form.")
    return render(request, 'owner_dashboard.html', {'product': product})


# @login_required
# def change_password_view(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('home')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'change_password.html', {'form': form})

# def get_purchase_history():
#     # Retrieve all purchase data
#     purchases = Purchase.objects.all().values('customer_id', 'product_id', 'quantity_purchased')
    
#     if not purchases:  
#         return pd.DataFrame(), pd.DataFrame()
    
#     df = pd.DataFrame(list(purchases))

   
#     purchase_matrix = df.pivot_table(index='customer_id', columns='product_id', values='quantity_purchased', fill_value=0)

  
#     item_similarity_matrix = cosine_similarity(purchase_matrix.T)

    
#     item_similarity_df = pd.DataFrame(item_similarity_matrix, index=purchase_matrix.columns, columns=purchase_matrix.columns)

#     return purchase_matrix, item_similarity_df


# def recommend_products(customer_id, purchase_matrix, item_similarity_df, top_n=2):
#     # Check if purchase matrix or customer ID does not exist
#     if purchase_matrix.empty or customer_id not in purchase_matrix.index:
#         return []
    
#     # Fetch the customer's purchase history
#     customer_purchases = purchase_matrix.loc[customer_id]

#     # Calculate similarity scores by multiplying item similarity matrix with customer's purchases
#     similar_scores = item_similarity_df.dot(customer_purchases).sort_values(ascending=False)

#     # Filter out products that the customer has already purchased
#     recommended_products = similar_scores[~customer_purchases.astype(bool)].head(top_n)

#     # Return the list of recommended product indices
#     return recommended_products.index.tolist()
def get_purchase_history():
    # Retrieve all purchase data including product category
    purchases = Purchase.objects.all().values('customer_id', 'product__category', 'quantity_purchased')

    if not purchases:
        return pd.DataFrame(), pd.DataFrame()
    
    # Convert purchase history to DataFrame
    df = pd.DataFrame(list(purchases))

    # Create a pivot table where rows are customers and columns are product categories
    purchase_matrix = df.pivot_table(index='customer_id', columns='product__category', values='quantity_purchased', fill_value=0)

    # Calculate cosine similarity between product categories
    category_similarity_matrix = cosine_similarity(purchase_matrix.T)

    # Create a DataFrame for category similarity
    category_similarity_df = pd.DataFrame(category_similarity_matrix, index=purchase_matrix.columns, columns=purchase_matrix.columns)

    return purchase_matrix, category_similarity_df


def recommend_products(customer_id, purchase_matrix, category_similarity_df, top_n=2):
    # Check if purchase matrix or customer ID does not exist
    if purchase_matrix.empty or customer_id not in purchase_matrix.index:
        return []
    
    # Fetch the customer's purchase history (based on product categories)
    customer_purchases = purchase_matrix.loc[customer_id]

    # Calculate similarity scores by multiplying category similarity matrix with customer's purchases
    similar_scores = category_similarity_df.dot(customer_purchases).sort_values(ascending=False)

    # Filter out categories that the customer has already purchased from
    recommended_categories = similar_scores[~customer_purchases.astype(bool)].head(top_n)

    # Return the list of recommended product categories
    return recommended_categories.index.tolist()


@login_required
def customer_dashboard(request):
    customer = Customer.objects.get(user=request.user)

    # Get all available products
    available_products = Product.objects.all()

    try:
        # Get the customer-product matrix and item similarity matrix
        purchase_matrix, item_similarity_df = get_purchase_history()

        # Get recommended products based on customer's purchase history
        recommended_product_ids = recommend_products(customer.id, purchase_matrix, item_similarity_df, top_n=2)

        # If no recommended products, return random products
        if not recommended_product_ids:
            # Provide fallback to show 5 random products as a recommendation
            recommended_products = Product.objects.order_by('?')[:1]
        else:
            # Filter recommended products based on the IDs
            recommended_products = Product.objects.filter(id__in=recommended_product_ids)
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error generating recommendations: {e}")

        # In case of an error, provide a fallback of 5 random products
        recommended_products = Product.objects.order_by('?')[:1]

    # Pass available products and recommended products to the context
    context = {
        'available_products': available_products,
        'recommended_products': recommended_products,
    }

    # Render the customer dashboard template with the context data
    return render(request, 'customer_dashboard.html', context)

@login_required
def add_to_cart_js(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Check if the product is still in stock
        if product.quantity <= 0:
            return JsonResponse({'error': 'Out of stock'}, status=400)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

       
        if created:
            cart_item.quantity = 1  # Set to 1 if new item is added
        else:
            cart_item.quantity += 1  # Increment quantity for existing item

        cart_item.save()

        # Decrease product stock
        product.quantity -= 1
        product.save()

        # Calculate the new total price
        total_price = sum(item.total_price() for item in cart.cartitem_set.all())

        return JsonResponse({
            'new_stock': product.quantity,
            'quantity': cart_item.quantity,
            'in_cart': True,
            'success': True,
            'total_price': total_price,
            'version': request.POST.get('version', 0)  # Pass the version back
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def decrease_quantity_js(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

    
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()  # Remove the item from the cart if the quantity is 1

        # Increase the product stock
        product.quantity += 1
        product.save()

        return JsonResponse({
            'new_stock': product.quantity,
            'quantity': cart_item.quantity if cart_item.quantity > 1 else 0,
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)



@login_required
@transaction.atomic  
def checkout_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if request.method == 'POST':
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('customer_dashboard')

        for cart_item in cart_items:
            product = cart_item.product

            # Ensure stock is available
            if product.quantity < cart_item.quantity:
                messages.error(request, f"Not enough stock for {product.name}.")
                return redirect('view_cart')

        # Proceed with the sale if everything is in stock
        for cart_item in cart_items:
            product = cart_item.product

            # # Deduct stock
            # product.quantity -= cart_item.quantity
            product.save()

            #Create a sale record
            customer = Customer.objects.get(user=request.user)
            # sale = Sales.objects.create(
            #     product=product,
            #     quantity_sold=cart_item.quantity,
            #     sale_date=datetime.now(),
            #     customer_id=request.user.id
            # )

         
            Purchase.objects.create(
                customer=customer,
                product=product,
                quantity_purchased=cart_item.quantity,
                purchase_date=datetime.now()
            )
        check_stock_and_alert(product)
     
        cart_items.delete()

        messages.success(request, "Your purchase was successful!")
        return redirect('customer_dashboard')


def forecast_next_5_days_with_padding(model, sales_df, lookback=10):
    quantity_values = sales_df['quantity_purchased'].values
    if len(quantity_values) < lookback:
        last_known_sales = np.pad(quantity_values, (lookback - len(quantity_values), 0), 'constant').reshape((1, lookback, 1))
    else:
        last_known_sales = quantity_values[-lookback:].reshape((1, lookback, 1))
    predictions = []
    for _ in range(5):
        predicted_sales = model.predict(last_known_sales)
        predictions.append(predicted_sales[0][0])
        new_input = np.append(last_known_sales[0, 1:], predicted_sales[0])
        last_known_sales = new_input.reshape((1, lookback, 1))
    return predictions

def forecast_view(request):
    # Set random seed for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)

    
    purchased_products = Product.objects.filter(id__in=Product.objects.values('id').distinct())

    future_sales = None
    selected_product = None

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        selected_product = Product.objects.get(id=product_id )

 
        sales_data = Purchase.objects.filter(product=product_id).order_by('purchase_date')
        print(sales_data)
        if sales_data.exists():
    
            sales_df = pd.DataFrame(list(sales_data.values('purchase_date', 'quantity_purchased')))
            sales_df['sale_date'] = pd.to_datetime(sales_df['purchase_date'])
            BASE_DIR = 'smart_retail\retail_app'
            
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            model_path = os.path.join(BASE_DIR, 'my_model.keras')
    
   
            model = load_model(model_path)
            
            # Forecast future sales for the next 5 days
            forecasted_sales = forecast_next_5_days_with_padding(model, sales_df)
            print(forecasted_sales)

            # Prepare the sales forecast as a list for each of the next 5 days
            future_sales = [round(sale) for sale in forecasted_sales]
            today = datetime.now()

   
    return render(request, 'forecast.html', {
        'products': purchased_products,
        'future_sales': future_sales,
        'product': selected_product
    })


    from datetime import timedelta

def check_stock_and_alert(product):
    dynamic_threshold = calculate_dynamic_threshold(product)
    if product.quantity < dynamic_threshold:
        send_stock_alert(product, dynamic_threshold)

def calculate_dynamic_threshold(product, recent_days=7):
  
    recent_sales_start = timezone.now() - timedelta(days=recent_days)

    recent_sales = Sales.objects.filter(
        product=product,
        sale_date__gte=recent_sales_start
    ).aggregate(total_recent_sales=Sum('quantity_sold'))
    
  
    total_recent_sales = recent_sales['total_recent_sales'] or 0
    
    threshold = max(total_recent_sales * 2, 5)  
    
    return threshold

def send_stock_alert(product, dynamic_threshold):
    subject = f"Low Stock Alert: {product.name}"
    message = f"Product {product.name} is low on stock!\n" \
              f"Current quantity: {product.quantity}\n" \
              f"Dynamic threshold: {dynamic_threshold}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [settings.DEFAULT_FROM_EMAIL]
    send_mail(subject, message, from_email, recipient_list)


def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    print("User logged out.")
    return redirect('login_view') 