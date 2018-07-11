from django.urls import path 
from . import views
from .views import (
    LoginView, 
    RegisterView,
    CardHomeView, 
    AllCardsView,
    CardTypeView,
    CardSubtypeView,
    logout_view
)

urlpatterns = [
    
    path("", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),

    # Card Urls
    path("home", CardHomeView.as_view(), name="home"),
    path("all_cards", AllCardsView.as_view(), name="all_cards"),
    path("card_types", CardTypeView.as_view(), name="card_types"),
    path("card_subtypes", CardSubtypeView.as_view(), name="card_subtypes"),

    path('logout/', views.logout_view, name="logout")

]