from django.urls import path
from . import views

urlpatterns = [
    path('utilities/exchange/', views.exchange),
]
