
from django.urls import path, include
from . import views


urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logOutUser, name='logout'),
    path('user/', views.userPage, name="user-page"),

]