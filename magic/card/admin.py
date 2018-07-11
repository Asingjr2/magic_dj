from django.contrib import admin

from .models import MagicCard, Deck

admin.site.register(MagicCard)
admin.site.register(Deck)