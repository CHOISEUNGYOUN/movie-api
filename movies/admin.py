from django.contrib import admin

from . import models

@admin.register(models.Movie)
class MovieAdimin(admin.ModelAdmin):
    
    filter_horizontal = (
        "genres",
        "torrents"
    )

@admin.register(models.Torrent)
class TorrentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
