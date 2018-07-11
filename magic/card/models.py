from django.db import models
from django.contrib.auth.models import User

from base.models import BaseModel


# Create your models here.
class Card(BaseModel):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("card_detail", args(self.id,))


class Deck(BaseModel):
    deck_name = models.CharField(max_length=200),
    deck_card = models.ForeignKey(Card, on_delete=models.CASCADE)