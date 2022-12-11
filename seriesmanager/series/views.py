from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views import View

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
        saved = TVShowRate.objects.all().filter(user=request.user, title=data.name, description=data.description)
        if len(saved) > 0:
            saved=saved[0]
        else:
            saved = TVShowRate(user=request.user,
                                title=data.name,
                                rating=data.rating,
                                years=data.years,
                                countries=data.countries,
                                genres=data.genres,
                                description=data.description,
                                isInList=False)    
            saved.save()

        if saved.isInList:
            return redirect("series_info", saved.pk)

        context = {'series_result': series_result,
                                               'series_name': series_name,
                                               'series_rating': series_rating,
                                               'series_years': series_years,
                                               'series_countries': series_countries,
                                               'series_genres': series_genres,
                                               'series_description': series_description,
                                               'id' : saved.id}
        context.update(self.get_context_mixin(request=self.request))
        current_series.update(context)
        return redirect("series_add")

def modify(request, id, action):
    saved = TVShowRate.objects.get(pk=id)
    if action == "add":
        saved.isInList = True
        saved.save()
    elif action == "delete":
        saved.delete()

    return redirect('profile')

class ProfileView(LoginRequiredMixin, Mixin, View):
    def get(self, request):
        context = dict()
        context.update(self.get_context_mixin(request=self.request))
        TVShowRate.objects.all().filter(user = request.user, isInList=False).delete()
        saved = TVShowRate.objects.all().filter(user = request.user)
        context.update({'series' : saved})
        return render(request, 'profile.html', context)

class SeriesInfoView(LoginRequiredMixin, Mixin, TemplateView):
    template_name = "series_info.html"

    def get_context_data(self, id, request=None, **kwargs):
        context = super(SeriesInfoView, self).get_context_data(**kwargs)
        context.update(self.get_context_mixin(request=self.request, **kwargs))
        saved = TVShowRate.objects.get(pk=id)
        current_series.clear()
        current_series.update({'series_name': saved.title,
                                               'series_rating': saved.rating,
                                               'series_years': saved.years,
                                               'series_countries': saved.countries,
                                               'series_genres': saved.genres,
                                               'series_description': saved.description,
                                               'id': saved.id})
        context.update(current_series)
        context.update({'series_result': 'Сериал из списка:',
                        'isInList': saved.isInList,
                        'series_score': saved.score})

        return context


class SeriesAddView(LoginRequiredMixin, Mixin, TemplateView):
    template_name = "series_add.html"

    def get_context_data(self, action=None, request=None, **kwargs):
        context = super(SeriesAddView, self).get_context_data(**kwargs)
        context.update(self.get_context_mixin(request=self.request, **kwargs))
        context.update(current_series)
        context['form'] = ScoreForm
        context['change'] = False
        if action == "change":
            context['change'] = True
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        saved = TVShowRate.objects.all().filter(user=request.user,
                                                title=current_series['series_name'],
                                                description=current_series['series_description'])
        saved = saved[0]
        if request.POST['series_score']:
            saved.score = int(request.POST['series_score'])
        saved.save()
        return redirect("modify", id=saved.pk, action="add")
