from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('delete/', views.delete),
    path('user/', views.get_user_info),
    path('update/', views.update_user_info),
    path('financial-score/', views.calculate_financial_score, name='calculate_financial_score'),
    path('get-financial-score/', views.get_financial_score, name='get_financial_score'),
]
