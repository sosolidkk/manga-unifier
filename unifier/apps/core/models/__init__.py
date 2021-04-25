from django.contrib.auth import get_user_model
from unifier.apps.core.models.base import StandardModelMixin
from unifier.apps.core.models.chapter import MangaChapter, NovelChapter
from unifier.apps.core.models.manga import Manga
from unifier.apps.core.models.novel import Novel
from unifier.apps.core.models.plataform import Platform
from unifier.apps.core.models.user import Favorite

User = get_user_model()
