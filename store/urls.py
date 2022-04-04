
from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('recharge/', views.recharge, name="recharge"),
	path('register/', views.register, name="register"),

	path('product/<str:pk>/', views.product, name="product"),
	path('delete_event/<str:pk>/', views.delete_event, name="delete_event"),
]
