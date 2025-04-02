from django.urls import include, path
from . import views

urlpatterns = [
    path('users', views.user, name="users_view"),
    path('login', views.login, name="login_view")
]