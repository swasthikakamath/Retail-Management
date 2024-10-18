import random
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from retail_app.models import Product

class Command(BaseCommand):
    help = 'Generates 30 random products with images'

    def handle(self, *args, **kwargs):
        categories = ['FR', 'DA', 'BV', 'SN', 'CL', 'PH', 'OT']
        product_names = [
            'Apple', 'Banana', 'Milk', 'Orange Juice', 'Bread', 'Butter', 'Chips', 
            'Soda', 'Shampoo', 'Soap', 'Toothpaste', 'Lettuce', 'Tomato', 'Chicken', 
            'Cheese', 'Yogurt', 'Coffee', 'Tea', 'Cereal', 'Rice', 'Pasta', 'Sugar', 
            'Salt', 'Peanut Butter', 'Jam', 'Eggs', 'Carrots', 'Cabbage', 'Potatoes', 'Spinach'
        ]
        
        image_folder = os.path.join(settings.MEDIA_ROOT, 'products')
        image_files = os.listdir(image_folder)  # List all images in the folder

        for _ in range(30):
            name = random.choice(product_names)
            quantity = random.randint(1, 100)
            price = round(random.uniform(1.00, 20.00), 2)
            category = random.choice(categories)
           
            image_path = 'F:\Projects\Retail Management System\smart_retail\retail_app\products\download.png'  # Path relative to MEDIA_ROOT

            Product.objects.create(
                name=name,
                quantity=quantity,
                price=price,
                category=category,
                image=image_path
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated 30 random products with images'))
