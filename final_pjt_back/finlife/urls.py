from django.urls import path
from . import views

urlpatterns = [
    path('utilities/exchange/', views.exchange),
    path('library/books/', views.get_economic_books),
    path('save-deposit-products/', views.save_deposit_products),
    path('save-saving-products/', views.save_saving_products),
    path('deposit-products/', views.get_deposit_products),
    path('saving-products/', views.get_saving_products),
]
