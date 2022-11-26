from .models import *

enter_menu = [{"title" : "Sign in", "url" : "login"},
        {"title" : "Sign up", "url" : "registration"},
        {"title" : "Home", "url" : "home"}]

exit_menu = [{"title" : "Logout", "url" : "logout"},
             {"title" : "Home", "url" : "home"}]


class Mixin:
    def get_context_mixin(self, request=None, **kwargs):
        context = kwargs
        if request and request.user.is_authenticated:
            context["menu"] = exit_menu
        else:
            context["menu"] = enter_menu
        return context