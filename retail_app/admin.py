
# Register your models here.
from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Product)
admin.site.register(Sales)
admin.site.register(Customer)
admin.site.register(Purchase)
admin.site.register(Cart)
admin.site.register(CartItem)        
