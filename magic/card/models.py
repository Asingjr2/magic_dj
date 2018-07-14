from django.db import models
from django.contrib.auth.models import User

from base.models import BaseModel


# Optional attribute on card
class TriggeredAbility(BaseModel):
    t_ability_name = models.CharField(max_length=200, default="n/a")

    def __str__(self):
        return self.t_ability_name


# Optional attribute on card
class ActivatedAbility(BaseModel):
    a_ability_name = models.CharField(max_length=200, default="n/a")

    def __str__(self):
        return self.a_ability_name


class MagicCard(BaseModel):
    name = models.CharField(max_length=100, default="n/a")
    quote = models.CharField(max_length=200, default="n/a")
    year = models.CharField(max_length=200, default="n/a")
    mana = models.IntegerField(default=0)
    card_set = models.CharField(max_length=200, default="n/a")
    # May be a list of abilites so creating new class
    triggered_ability = models.ForeignKey(TriggeredAbility, on_delete=models.CASCADE, null=True)
    activated_ability = models.ForeignKey(ActivatedAbility, on_delete=models.CASCADE, null=True)
    card_type = models.CharField(max_length=100, default="n/a")

    def __str__(self):
        return self.name


class Deck(BaseModel):
    deck_name = models.CharField(max_length=200, default="New Deck")
    card = models.ForeignKey(MagicCard, blank=True, null=True, on_delete=models.CASCADE)
    deck_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

