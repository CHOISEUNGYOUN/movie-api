from django.contrib import admin

from . import models

class TorrentInline(admin.TabularInline):
    
    model = models.Torrent

@admin.register(models.Movie)
class MovieAdimin(admin.ModelAdmin):
    
    inlines = (TorrentInline, )

    filter_horizontal = (
        "genres",
    )

@admin.register(models.Torrent)
class TorrentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
