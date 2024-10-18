from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register_view'),
    path('home/', views.home, name='home'),
    path('customer_dashboard/',views.customer_dashboard,name='customer_dashboard'),
    path('owner_dashboard/',views.owner_dashboard,name='owner_dashboard'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('add_to_cart_js/', views.add_to_cart_js, name='add_to_cart_js'),
    path('decrease_quantity_js/', views.decrease_quantity_js, name='decrease_quantity_js'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout_view/', views.checkout_view, name='checkout_view'),
    path('sales/', views.view_sales, name='view_sales'),
    # path('owner_dashboard/sales_trend_view/', views.sales_trend_view, name='sales_trend_view'),
    path('owner_dashboard/forecast_view/', views.forecast_view, name='forecast_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)