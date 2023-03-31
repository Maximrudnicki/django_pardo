from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Word


class WordAccessMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Word.objects.by_user(self.request.user)
