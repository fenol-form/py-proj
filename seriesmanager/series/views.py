from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .models import *

from .forms import *

from .utils import *


class Home(Mixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data()
        context.update(self.get_context_mixin(request=self.request, **kwargs))
        return context


class Registration(CreateView):
    form_class = NewUserForm
    template_name = "registration.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = enter_menu
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class Login(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = enter_menu
        return context

    def get_success_url(self):
        return reverse_lazy("home")


def sign_out(request):
    logout(request)
    return redirect("home")


class ResultPage(LoginRequiredMixin, Mixin, FormView):
    template_name = "result.html"

    def get_context_data(self, **kwargs):
        context = super(ResultPage, self).get_context_data(**kwargs)
        context.update(self.get_context_mixin(request=self.request, **kwargs))
        return context


class SearchPage(LoginRequiredMixin, Mixin, FormView):
    form_class = SearchForm
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchPage, self).get_context_data(**kwargs)
        context.update(self.get_context_mixin(request=self.request, **kwargs))
        return context

    def post(self, request, *args, **kwargs):
        data = parse(request.POST['series_name'])
        series_result = data.result
        series_name = data.name
        series_rating = f"Рейтинг: {data.rating}"
        series_years = f"Годы съёмки: {data.years}"
        series_countries = f"Страны съёмки: {data.countries}"
        series_genres = f"Жанры: {data.genres}"
        series_description = data.description
        return render(request, 'result.html', {'series_result': series_result,
                                               'series_name': series_name,
                                               'series_rating': series_rating,
                                               'series_years': series_years,
                                               'series_countries': series_countries,
                                               'series_genres': series_genres,
                                               'series_description': series_description})


    
