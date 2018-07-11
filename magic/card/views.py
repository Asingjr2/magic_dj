from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic.detail import DetailView

from mtgsdk import Card
from mtgsdk import Type
from mtgsdk import Subtype

from .forms import RegisterForm, LoginForm


# Create your views here.
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
            print("valid")
            return redirect("/login")
        else:
            if 'username' in form.errors:
                messages.warning(request, 'Username does not meet requirements.  Please try again.')
            if 'password' in form.errors:
                messages.warning(request, 'Passwrod does not meet requirements.  Please try again.')
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
        context = {
            "card": test_card , 
            "card_type_total": len(Type.all()), 
            "card_subtype_total" : len(Subtype.all()) 
        }
        print("card result {}".format(test_card))
        return render(request, self.template_name, context)


# Total number of cards including foreign is 36938!!!!
class AllCardsView(View):
    template_name = "card/all_cards.html"

    def get(self, request):
        # Pulling all cards count is demanding and would load slow.  Probably best to due asynchonously.  Not sure whether to house in session or DB.
        # all_cards_set = Card.all()
        all_cards = Card.where(page=5).where(pageSize=6).all()
        context = {
            "all_cards" : all_cards,
            "card_type_total": len(Type.all()), 
            "card_subtype_total" : len(Subtype.all())  
        }
        print("all cards{}".format(all_cards))
        return render(request, self.template_name, context)


class CardTypeView(View):
    template_name = "card/type.html"

    def get(self, request):
        card_types = Type.all()
        context = {
            "types" : card_types,
            "card_type_total": len(Type.all()), 
            "card_subtype_total" : len(Subtype.all())  
        }
        print("card types {}".format(card_types))
        return render(request, self.template_name, context)


class CardSubtypeView(View):
    template_name = "card/subtype.html"

    def get(self, request):
        card_subtypes = Subtype.all()
        context = {
            "subtypes" : card_subtypes,
            "card_type_total": len(Type.all()), 
            "card_subtype_total" : len(Subtype.all())   
        }
        print("card subtypes {}".format(card_subtypes))
        return render(request, self.template_name, context)


def logout_view(request):
    """ Clears session data created at login"""
    logout(request)
    return redirect("/login")
