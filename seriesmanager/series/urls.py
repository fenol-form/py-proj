from django.urls import path, include

from .views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("login/", Login.as_view(), name="login"),
    path("registration", Registration.as_view(), name="registration"),
    path("logout", sign_out, name="logout"),
    path("search", SearchPage.as_view(), name="search"),
    path("result", ResultPage.as_view(), name="result"),
    path("modify/<int:id>/<action>", modify, name="modify"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("series_info/<int:id>", SeriesInfoView.as_view(), name="series_info"),
    path("series_add", SeriesAddView.as_view(), name="series_add"),
    path("series_add/<action>", SeriesAddView.as_view(), name="series_add"),
]
