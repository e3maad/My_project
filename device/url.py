from django.urls import path
from . import views

urlpatterns = [
    path('showdevice/',views.showdevice,name='showdevice'),
    path('details_V/<int:id>/',views.details_V,name='details_V'),
    path('auth_register/',views.auth_register,name='auth_register'),
    path('auth_login/',views.auth_login,name='auth_login'),
    path('auth_logout/',views.auth_logout,name='auth_logout'),
    path('checkout_V/',views.checkout_V,name='checkout_V'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
]