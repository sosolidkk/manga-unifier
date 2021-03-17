import secrets
import string

import factory
from django.contrib.auth.models import User
from faker import Faker

faker = Faker("pt_BR")

ALPHABET = string.ascii_letters + string.digits


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = faker.ascii_email()
    password = "".join(secrets.choice(ALPHABET) for i in range(20))
    username = factory.LazyAttribute(lambda _: faker.simple_profile()["username"])
    first_name = faker.first_name()
    last_name = faker.last_name()


class AdminUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = faker.ascii_email()
    password = "".join(secrets.choice(ALPHABET) for i in range(20))
    username = factory.LazyAttribute(lambda _: faker.simple_profile()["username"])
    first_name = faker.first_name()
    last_name = faker.last_name()

    is_superuser = True
    is_staff = True
    is_active = True
