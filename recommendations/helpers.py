from .models import Movie, Recommendation
from .choices import LANGUAGES


def make_new_recommendation(user):
    recommendation = Recommendation(user_id=user)
    recommendation.save()  # needs id

    all_movies = Movie.objects.all()
    recommendation.possible_films.set(all_movies)
    recommendation.possible_film_count = len(all_movies)
    recommendation.save()
    return recommendation


# TODO only works for genre, year, runtime, language (untested)
def recommendation_querying(recommendation, field, selection):
    if field == "year" or field == "runtime":
        span = selection.split("-")
        return recommendation.possible_films.filter(
            **{f"{field}__gte": span[0]}, **{f"{field}__lte": span[1]}
        )
    elif field == "language":
        return recommendation.possible_films.filter(language__in=selection)

    # genre
    return recommendation.possible_films.filter(**{f"{field}__contains": selection})


# make arrays strings, make choices human readable, etc.
def make_readable_recommendation(recommended_films):
    readable_recommendation = []
    for film in recommended_films:
        readable_film = {
            "id": film.id,
            "name": film.name,
            "poster": film.poster,
            "year": film.year,
            "language": "",
            "genre": "",
            "director": "",
        }

        language_dict = dict(LANGUAGES)  # thanks chatgpt
        readable_film["language"] = language_dict.get(film.language)

        readable_film["genres"] = (", ").join(film.genres)
        readable_film["director"] = (", ").join(film.director)

        readable_recommendation.append(readable_film)

    return readable_recommendation
