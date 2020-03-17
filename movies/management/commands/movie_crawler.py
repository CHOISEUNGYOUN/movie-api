import requests, time

from django.core.management.base import BaseCommand

from movies import models as movie_models

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--page", default=1, type=int, help="page info"
        )

    def handle(self, *args, **options):
        page = options.get("page")
        genres = movie_models.Genre.objects.all()
        torrents = movie_models.Torrent.objects.all()
        page_url = "https://yts.mx/api/v2/list_movies.json"
        movie_page = requests.get(page_url+f"?page={page}")
        time.sleep(2)
        json_data = movie_page.json()["data"]
        movie_data = json_data["movies"]
        mpa_choices = movie_models.Movie.MPA_RATINGS
        for m in movie_data:
            new_m = movie_models.Movie.objects.create(
                url = m["url"],
                title = m["title"],
                title_english = m["title_english"],
                title_long = m["title_long"],
                year = int(m["year"]),
                rating = int(m["rating"]),
                runtime = int(m["runtime"]),
                summary = m["summary"],
                description_full = m["description_full"],
                synopsis = m["synopsis"],
                language = m["language"],
                mpa_rating = m["mpa_rating"],
                background_image = m["background_image"],
                background_image_original = m["background_image_original"],
                small_cover_image = m["small_cover_image"],
                medium_cover_image = m["medium_cover_image"],
                large_cover_image = m["large_cover_image"],
            )
            for g in m["genres"]:
                if movie_models.Genre.objects.filter(genres=g).exists():
                    new_g = movie_models.Genre.objects.get(genres=g)
                else:
                    new_g = movie_models.Genre.objects.create(genres=g)
                new_m.genres.add(new_g)

            for t in m["torrents"]:
                if movie_models.Torrent.objects.filter(url=t["url"]).exists():
                    new_t = movie_models.Torrent.objects.get(url=t["url"])
                else:
                    new_t = movie_models.Torrent.objects.create(
                        movie = new_m,
                        url = t["url"],
                        quality = t["quality"],
                        type = t["type"],
                        seeds = t["seeds"],
                        peers = t["peers"],
                        size = t["size"],
                        size_bytes = t["size_bytes"],
                    )
