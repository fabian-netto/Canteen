
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),

    path('recharge/', views.recharge, name="recharge"),
    path('auth_recharge/', views.auth_recharge, name="auth_recharge"),
    path('detail_recharge/', views.detail_recharge, name="detail_recharge"),

    path('user_not/', views.user_not, name="user_not"),
    path('device_not/', views.device_not, name="device_not"),
    path('device_busy/', views.device_busy, name="device_busy"),
    path('timeout/', views.timeout, name="timeout"),
    path('insuff_bal/', views.insuff_bal, name="insuff_bal"),
    path('payment/', views.payment, name="payment"),

    path('recharge_timeout/', views.recharge_timeout, name="recharge_timeout"),
    path('register_timeout/', views.register_timeout,
         name="register_timeout"),


    path('register/', views.register, name="register"),
    path('auth_register/', views.auth_register, name="auth_register"),
    path('registration_success/', views.registration_success,
         name="registration_success"),

    path('checkout/', views.checkout, name="checkout"),
    path('detail/', views.detail, name="detail"),
    path('reciept/', views.reciept, name="reciept"),

    path('product/<str:pk>/', views.product, name="product"),
    path('delete_event/<str:pk>/', views.delete_event, name="delete_event"),
]
