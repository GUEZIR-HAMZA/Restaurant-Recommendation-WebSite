from operator import index

from django.urls import path

from Restaurant_Recommendation_WebSite.views import auth, user_logout

urlpatterns = [
    path("index/", index, name='index'),
    path("auth/", auth, name='auth.html'),
    path('logout/', user_logout, name='logout'),
]


