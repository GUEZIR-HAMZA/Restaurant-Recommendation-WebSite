from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('restaurant_details/<int:restaurant_id>/', views.restaurant_details, name='restaurant_details'),
    path('search/', views.search_view, name='search'),
]


