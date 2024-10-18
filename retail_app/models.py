from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


def custom_email_validator(value):
    if "@" not in value:
        raise ValidationError("Please include an '@' in the email address.")
    if "gmail" not in value:
        raise ValidationError("Please include an 'gmail' in the email address.")
    elif not value.endswith('.com'):
        raise ValidationError("Email must end with '.com'.")
    

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(validators=[custom_email_validator], widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('FR', 'Fresh Produce'),
        ('DA', 'Dairy'),
        ('BV', 'Beverages'),
        ('SN', 'Snacks'),
        ('CL', 'Cleaning Supplies'),
        ('PH', 'Pharmacy'),
        ('BP', 'Beauty Products'),
        ('OT', 'Other')
    ]

    name = models.CharField(max_length=255, unique=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='smart_retail/retail_app/static/media', blank=False)
# class Category(models.Model):
#     name = models.CharField(max_length=255, unique=True)

#     def __str__(self):
#         return self.name
    
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Updated to use Category model
#     image = models.ImageField(upload_to='products/', default='products/default.jpg', blank=True)

#     def __str__(self):
#         return self.name




class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    purchase_history = models.ManyToManyField('Product', through='Purchase')

    def clean(self):
        # Ensure that the user has the "customer" role
        if self.user.profile.role != 'customer':
            raise ValidationError('Only users with the role of "customer" can be linked to a customer profile.')

    def __str__(self):
        return self.user.username
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s Cart"
class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} in {self.cart.user}'s cart"
    
    def total_price(self):
        return self.product.price * self.quantity

class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_purchased = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('customer', 'Customer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.user.username} ({self.role})"
