from django.urls import path
from accounts import views


urlpatterns = [
    path('user_login', views.user_Login , name='user_login'),
    path('user_register', views.user_register , name='user_register'),
    path('user_logout', views.user_Logout , name='user_logout'),
]
