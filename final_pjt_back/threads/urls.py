from django.urls import path
from . import views

urlpatterns = [
    path('', views.thread_list),
    path('<int:thread_pk>/', views.thread_detail),
    path('<int:thread_id>/like/', views.thread_like),
    path('<int:thread_pk>/comments/', views.comment_list),
    path('<int:thread_pk>/comments/create/', views.comment_create),
    path('<int:thread_pk>/comments/<int:comment_pk>/', views.comment_detail),
]
