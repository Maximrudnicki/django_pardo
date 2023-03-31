from django.contrib import admin

from .models import Word


class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'definition',
                    'user_with_username', 'learned', 'added')

    def user_with_username(self, obj):
        return obj.user.username
    user_with_username.short_description = 'User'


admin.site.register(Word, WordAdmin)
