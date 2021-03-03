from decimal import Decimal

import factory
from unifier.apps.core.models import Manga


class MangaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Manga

    title = "The Beginning After The End"
    year = 2018
    chapters_count = 92
    author = "TurtleMe"
    description = (
        "King Grey has unrivaled strength, wealth, and prestige in a world governed through martial ability. "
        "However, solitude lingers closely behind those with great power. Beneath the glamorous exterior of a powerful "
        "king lurks the shell of a man, devoid of purpose and will. Reincarnated into a new world filled with magic and"
        " monsters, the king has a second chance to relive his life. Correcting the mistakes of his past will not be "
        "his only challenge, however. Underneath the peace and prosperity of the new world is an undercurrent "
        "threatening to destroy everything he has worked for, questioning his role and reason for being born again."
    )
    rate = Decimal(4.80)
    status = "OnGoing"
    cover = "https://www.webtoon.xyz/wp-content/uploads/2020/05/The-Beginning-After-the-End-193x278.jpg"
    tags = ["Action", " Adventure", " Comedy", " Drama", " Fantasy"]
