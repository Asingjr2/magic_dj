from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic.detail import DetailView
# Cache module used to set card, type, and subtype list
from django.core.cache import cache

from django.core import serializers
from django.http import JsonResponse

import requests

from mtgsdk import Card
from mtgsdk import Type
from mtgsdk import Subtype

from .forms import RegisterForm, LoginForm


# Generic views will not be in final version
class RegisterView(View):
    form_class = RegisterForm
    template_name = "card/reg.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        """ Overriding base post method to encrpyt user password and validate registration from data"""
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            return redirect("/login")
        else:
            if 'username' in form.errors:
                messages.warning(request, 'Username does not meet requirements.  Please try again.')
            if 'password' in form.errors:
                messages.warning(request, 'Password does not meet requirements.  Please try again.')
            return redirect("/")


class LoginView(View):
    form_class = LoginForm
    template_name = "card/log.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form":form})
    
    def post(self, request):
        form = LoginForm()
        submitted_form = self.form_class(request.POST)

        if submitted_form.is_valid():
            try: 
                username = submitted_form.cleaned_data["username"]
                password = submitted_form.cleaned_data["password"]
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user)
                    """
                    Querying MTG DB for random 200 cards vs entire collection of 37000.
                    Could query asynchonously to save time or save one through caching and then move to static files during production???
                    """
                    cache.set("small_card_set", Card.where(page=1).where(pageSize=20, random=True).all(), 200)
                    # Setting total card type in cache
                    cache.set("card_type_total",Type.all(), 200)
                    # Setting total card substype in cache
                    cache.set("card_subtype_total",Subtype.all(), 200)
                    return redirect("/home")
                else:
                    messages.warning(request, 'Username or password does not match our records')
                    return redirect("/login")
            except: 
                messages.warning(request, 'Username or password does not match our records')
                return render(request, self.template_name, {"form":form})


class CardHomeView(View):
    template_name = "card/home.html"

    def get(self, request):
        test_card = Card.find(386616)
        # Additional context use to populate spans set in cache to avoid redundant queries
        context = {
            "card" : test_card,
            "card_type_total": len(cache.get("card_type_total")), 
            "card_subtype_total" : len(cache.get("card_subtype_total")) 
        }
        return render(request, self.template_name, context)


class AllCardsView(View):
    """ Pulled 100 cards of total number of 36938!!!! """
    template_name = "card/all_cards.html"

    def get(self, request):
        context = {
            "card_set" : cache.get("small_card_set"),
            "card_type_total_set" : cache.get("card_type_total"),
            "card_type_total" : len(cache.get("card_type_total")), 
            "card_subtype_total" : len(cache.get("card_subtype_total"))  
        }
        
        return render(request, self.template_name, context)


class CardTypeView(View):
    template_name = "card/type.html"

    def get(self, request):
        card_types = Type.all()
        context = {
            "types" : card_types,
            "card_type_total": len(cache.get("card_type_total")), 
            "card_subtype_total" : len(cache.get("card_subtype_total"))   
        }
        print("card types {}".format(card_types))
        print("card types from cache {}".format(cache.get("card_type_total")))
        return render(request, self.template_name, context)


class CardSubtypeView(View):
    template_name = "card/subtype.html"

    def get(self, request):
        card_subtypes = cache.get("card_subtype_total")
        context = {
            "subtypes" : card_subtypes,
            "card_type_total": len(cache.get("card_type_total")), 
            "card_subtype_total" : len(cache.get("card_subtype_total"))   
        }
        print("card subtypes {}".format(card_subtypes))
        return render(request, self.template_name, context)


def logout_view(request):
    """ Clears session data created at login"""
    logout(request)
    return redirect("/login")
