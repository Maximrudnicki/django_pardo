from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class WordQuerySet(models.QuerySet):
    def by_user(self, user):
        return self.filter(user=user)


class WordManager(models.Manager):
    def get_queryset(self):
        return WordQuerySet(self.model, using=self._db)

    def by_user(self, user):
        return self.get_queryset().by_user(user)


class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    definition = models.CharField(max_length=255)
    learned = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)

    objects = WordManager()

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return f"{self.word} - {self.definition}"
    