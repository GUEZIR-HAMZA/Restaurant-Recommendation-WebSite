from django.contrib.auth import views as auth_views

from django.urls import path
from .views import *

from Restaurant_Recommendation_WebSite.views import auth, user_logout

urlpatterns = [
    path("", home, name='index'),
    path("auth/", auth, name='auth'),
    path('logout/', auth_views.auth_logout, name='logout'),
    path('restaurant_details/<int:restaurant_id>/', restaurant_details, name='restaurant_details'),

    # path("login/", auth_views.LoginView.as_view(), {'template_name': 'auth.html'}, name='Sign in'),
    # path("register/", RegisterView.as_view(), {'template_name': 'auth.html'}, name='Sign up'),
]


