
from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),

	path('recharge/', views.recharge, name="recharge"),
	path('auth_recharge/', views.auth_recharge, name="auth_recharge"),
	path('detail_recharge/', views.detail_recharge, name="detail_recharge"),


	path('register/', views.register, name="register"),
	path('auth_register/', views.auth_register, name="auth_register"),

	path('checkout/', views.checkout, name="checkout"),
	path('detail/', views.detail, name="detail"),
	path('reciept/', views.reciept, name="reciept"),

	path('product/<str:pk>/', views.product, name="product"),
	path('delete_event/<str:pk>/', views.delete_event, name="delete_event"),
]
