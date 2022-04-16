from django.urls import path, include

from . import views

urlpatterns = [
    path('user/<int:id>/balance', views.getBalance),
    path('user/<int:id>/deposit', views.depositFunds),
    path('user/<int:id>/charge', views.chargeFunds)
]