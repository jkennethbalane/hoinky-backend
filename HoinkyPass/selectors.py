from .models import Quest, HoinkyUser
from django.shortcuts import get_object_or_404


def get_quests():
    return Quest.objects.all()

def finished_quests(*args, **kwargs):
    hoinky_user = HoinkyUser.objects.get(pk=kwargs.get("user").id)
    return hoinky_user.quests_achieved.all()

def unfinished_quests(*args, **kwargs):
    hoinky_user = HoinkyUser.objects.get(pk=kwargs.get("user").id)
    quests = Quest.objects.all()
    achieved = hoinky_user.quests_achieved.all()
    return quests.difference(achieved)

def get_users(*args, **kwargs):
    hoinky_user = HoinkyUser.objects.all()
    return hoinky_user

def get_detail(qr, *args, **kwargs):
    hoinky_user = get_object_or_404(HoinkyUser, qr_unique = qr)
    return hoinky_user