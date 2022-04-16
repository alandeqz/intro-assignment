from django.urls import path, include

from . import views

urlpatterns = [
    path('order/create', views.createOrder),
    path('order/<int:id>', views.getOrderByID),
    path('orders', views.getOrders),
    path('order/pay', views.payOrder),
    path('order/<int:id>/refund', views.refundOrder),
    path('user/<int:id>/orders', views.getUserOrders)
]