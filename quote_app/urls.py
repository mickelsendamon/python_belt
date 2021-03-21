from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('home/', views.home),
    path('add_quote/', views.add_quote),
    path('delete_quote/<int:quote_id>/', views.delete_quote),
    path('like/<int:quote_id>/', views.like_quote),
    path('user/<int:user_id>/', views.view_user),
    path('myaccount/<int:user_id>', views.my_account),
    path('myaccount/update/', views.update_account),
]
