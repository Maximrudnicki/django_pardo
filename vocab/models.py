from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    definition = models.CharField(max_length=255)
    learned = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return f"{self.word} - {self.definition}"