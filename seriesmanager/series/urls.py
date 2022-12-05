from django.urls import path, include

from .views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("login/", Login.as_view(), name="login"),
    path("registration", Registration.as_view(), name="registration"),
    path("logout", sign_out, name="logout"),
    path("search", SearchPage.as_view(), name="search"),
    path("result", ResultPage.as_view(), name="result")
]
