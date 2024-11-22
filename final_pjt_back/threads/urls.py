from django.urls import path
from . import views

urlpatterns = [
    path('', views.thread_list),
    path('<int:thread_pk>/', views.thread_detail),
    path('<int:thread_pk>/comments/', views.comment_create),
]
