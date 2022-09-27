from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import ListView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/',views.loginUser, name='login'),
    path('register/',views.registerUser, name='register'),
    path('logout/',views.logoutUser, name='logout'),
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path('seller/', views.seller, name='seller'),
    path('/product/<slug:pk>', views.products, name='view-item'),
    path('cart/', views.cart, name='cart'),
    path('/cart2/<slug:pk>', views.cart2, name='cart2'),
    path('/cart3/<slug:pk>', views.cart3, name='cart3'),
    path('/add/<slug:pk>', views.add, name='add'),
    path('/sub/<slug:pk>', views.sub, name='sub'),
    path('/checkout/', views.checkout, name='checkout'),
    path('/checkout/<slug:pk>', views.checkout2, name='checkout2'),
    path('delete/<slug:pk>/',views.delete_item, name = 'delete'), 
]
