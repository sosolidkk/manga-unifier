from decimal import Decimal

import factory
from unifier.apps.core.models import Novel


class NovelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Novel

    title = "Tales of Demons and Gods"
    year = 2012
    chapters_count = 495
    author = "Mad Snail"
    description = (
        "Killed by a Sage Emperor and reborn as his 13 year old self, Nie Li was given a second chance at life."
        " A second chance to change everything, save his loved ones and his beloved city. He shall once again battle"
        " with the Sage Emperor to avenge his death. With the vast knowledge he accumulated in his previous life,"
        " he shall have a new starting point. Although he started as the weakest, without a doubt, he will climb"
        " the steps towards the strongest."
        "Cultivating the strongest cultivation technique, wielding the strongest demon spirits, he shall reach"
        " the pinnacle of Martial Arts. Enmities of the past will be settled in this new lifetime."
        "“Since I’m back, then in this lifetime, I shall become the King of Gods that dominates everything."
        " Let everything else tremble beneath my feet!”"
    )
    rate = Decimal(4.10)
    status = "OnGoing"
    cover = "https://cdn.wuxiaworld.com/images/covers/tdg.jpg?ver=9ad2e575c0daf4585acaa59f2c4b4b5b289c6864"
