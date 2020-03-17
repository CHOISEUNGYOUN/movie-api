from django.db import models
from django.utils.text import slugify

from languages.fields import LanguageField

class Movie(models.Model):

    MPA_RATINGS = {
        "G"     : "G",
        "PG"    : "PG",
        "PG-13" : "PG-13",
        "R"     : "R",
        "NC-17" : "NC-17"
    }

    MPA_CHOICES = (
        (MPA_RATINGS["G"],     "G"),
        (MPA_RATINGS["PG"],    "PG"),
        (MPA_RATINGS["PG-13"], "PG-13"),
        (MPA_RATINGS["R"],     "R"),
        (MPA_RATINGS["NC-17"], "NC-17")
    )
    
    url                       = models.URLField(max_length=500, null=True)
    title                     = models.CharField(max_length=100, null=False)
    title_english             = models.CharField(max_length=100, null=True, default='')
    title_long                = models.CharField(max_length=100, null=True, default='')
    slug                      = models.SlugField(max_length=100, null=True, default='')
    year                      = models.PositiveSmallIntegerField(null=False)
    rating                    = models.PositiveSmallIntegerField(null=False)
    runtime                   = models.PositiveSmallIntegerField(null=True, default=0)
    summary                   = models.TextField(null=False)
    description_full          = models.TextField(null=True, default='')
    synopsis                  = models.TextField(null=True)
    language                  = LanguageField(max_length=20, default="English")
    mpa_rating                = models.CharField(max_length=10, choices=MPA_CHOICES, default=MPA_RATINGS["R"])
    background_image          = models.URLField(max_length=500, null=True)
    background_image_original = models.URLField(max_length=500, null=True)
    small_cover_image         = models.URLField(max_length=500, null=True)
    medium_cover_image        = models.URLField(max_length=500, null=True)
    large_cover_image         = models.URLField(max_length=500, null=True)
    genres                    = models.ManyToManyField("Genre")
    date_uploaded             = models.DateTimeField(auto_now_add=True)
    date_added                = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Genre(models.Model):
    
    genres        = models.CharField(max_length=10, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.genres

class Torrent(models.Model):
    movie         = models.ForeignKey("Movie", on_delete=models.CASCADE, null=True)
    url           = models.URLField(max_length=500, default='')
    quality       = models.CharField(max_length=20, default='')
    type          = models.CharField(max_length=20, default='')
    seeds         = models.PositiveSmallIntegerField(null=True, default=0)
    peers         = models.PositiveSmallIntegerField(null=True, default=0)
    size          = models.CharField(max_length=20, default='')
    size_bytes    = models.PositiveSmallIntegerField(null=True, default=0)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
