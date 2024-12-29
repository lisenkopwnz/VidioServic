from django.contrib import admin

from playlist.models import Playlist


@admin.register(Playlist)
class AdminPlaylist(admin.ModelAdmin):
    filter_horizontal = ['content']

    def get_form(self, request, obj=None, **kwargs):
        """Добавляем подсказку для поля name"""
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].help_text = ("Если вы не укажите название плейлиста,оно будет сгенерированно "
                                              "автоматчески")
        return form
