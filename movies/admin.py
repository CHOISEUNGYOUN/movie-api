from django.contrib import admin

from . import models

@admin.register(models.Movie)
class MovieAdimin(admin.ModelAdmin):
    
    filter_horizontal = (
        "genres",
        "torrents",
    )
