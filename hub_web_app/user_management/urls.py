from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.get_login, name="login"),
    path('register/', views.get_register, name ="register"),
    path('register/<email><username><password><confirm_password>/', views.create_user),
    path('login/<email><password>/', views.login_user),
]