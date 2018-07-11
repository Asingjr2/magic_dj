from django.db import models
from django.contrib.auth.models import User

from base.models import BaseModel


# Create your models here.
# class Card(BaseModel):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

#     # def get_absolute_url(self):
#     #     return reverse("card_detail", args(self.id,))

class MagicCard(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Deck(BaseModel):
    deck_name = models.CharField(max_length=200, default="New Deck")
    card = models.ForeignKey(MagicCard, blank=True, null=True, on_delete=models.CASCADE)
    deck_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)