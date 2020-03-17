import json

from django.http                  import JsonResponse
from django.views                 import View

from . import models

class MissingRequiredValue(Exception):
        pass

class MovieListView(View):

    REQUIRED_VALUES = (
        "title",
        "year",
        "rating",
        "summary",
        "genre",
    )

    def get(self, request):
        page        = int(request.GET.get('page', 1))
        limit       = int(request.GET.get('limit', 20))
        limit       = limit if limit <= 50 else 20
        end         = 0
        order_by    = request.GET.get("order_by", "desc")
        sort_by     = request.GET.get("sort_by", "date_added")
        movies      = models.Movie.objects.all()
        torrents    = models.Torrent.objects.all()
        movie_count = movies.count()
        filter_queries = request.GET
        movie_filter = {}
        torrent_filter = {}
        genre_filter = {}
        for k,v in filter_queries.items():
            if k == "quality":
                torrent_filter[k] = v
            if k == "minimum_rating":
                movie_filter[f] = v
            if k == "genre":
                genre = models.Genre.objects.get(genres=v).id
                movie_filter["genres"] = genre

        filtered_movie = movies.filter(**movie_filter)
        if order_by == "desc":
            filtered_movie = filtered_movie.order_by(f"-{sort_by}")
        else:
            filtered_movie = filtered_movie.order_by(f"{sort_by}")
        if page == 1:
            offset = 0
            end    = limit
        else:
            offset = (page - 1) * limit
            end    = page * limit

        data = [{
            "url"                       : m.url,
            "title"                     : m.title,
            "title_english"             : m.title_english,
            "title_long"                : m.title_long,
            "slug"                      : m.slug,
            "year"                      : m.year,
            "rating"                    : m.rating,
            "runtime"                   : m.runtime,
            "summary"                   : m.summary,
            "description_full"          : m.description_full,
            "synopsis"                  : m.synopsis,
            "language"                  : m.language,
            "mpa_rating"                : m.mpa_rating,
            "background_image"          : m.background_image,
            "background_image_original" : m.background_image_original,
            "small_cover_image"         : m.small_cover_image,
            "medium_cover_image"        : m.medium_cover_image,
            "large_cover_image"         : m.large_cover_image,
            "genres"                    : [ g["genres"] for g in m.genres.values() ],
            "torrents"                  : list(torrents.filter(movie=m.pk, **torrent_filter).values()),
            "date_uploaded"             : m.date_uploaded,
        } for m in filtered_movie[offset:end]]

        return JsonResponse(
            {
                "movie_count" : movie_count,
                "limit"       : limit,
                "page_number" : page,
                "data"        : data,
            },
            status = 200,
            safe   = False
        )
    
    def post(self, request):
        data = json.loads(request.body)
        try:
            for v in self.REQUIRED_VALUES:
                if v not in data:
                    raise MissingRequiredValue

            new_m = models.Movie.objects.create(
                url                       = data.get("url",""),
                title                     = data["title"],
                title_english             = data.get("title_english",""),
                title_long                = data.get("title_long",""),
                year                      = int(data["year"]),
                rating                    = int(data["rating"]),
                runtime                   = int(data.get("runtime",0)),
                summary                   = data["summary"],
                description_full          = data.get("description_full",""),
                synopsis                  = data.get("synopsis",""),
                language                  = data.get("language",""),
                mpa_rating                = data.get("mpa_rating",""),
                background_image          = data.get("background_image",""),
                background_image_original = data.get("background_image_original",""),
                small_cover_image         = data.get("small_cover_image",""),
                medium_cover_image        = data.get("medium_cover_image",""),
                large_cover_image         = data.get("large_cover_image",""),
            )
            if models.Genre.objects.filter(genres=data["genre"]).exists():
                genre = models.Genre.objects.get(genres=data["genre"])
            else:
                genre = models.Genre.objects.create(genres=data["genre"])
            new_m.genres.add(genre)

            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
        except MissingRequiredValue:
            return JsonResponse({"MESSAGE": "NO_REQUIRED_VALUE_IN_DATA"}, status=400)
