from django.http import HttpResponse
from csfd.scraper import populate, beautify
from csfd.model import DBModel
from django.shortcuts import render
from django import forms

db_model = DBModel()


class SearchForm(forms.Form):
    search_for = forms.CharField(max_length=100, label='Film')


def index(request):
    context = {'submitted': False}
    if 'search_for' in request.GET:
        form = SearchForm(request.GET)
        context = _search_for(request.GET['search_for'])
        context['submitted'] = True
    else:
        form = SearchForm()
    context.update({'form': form})

    return render(request, 'index.html', context=context)


def _search_for(search_query):
    original_search_query = search_query.replace('-', ' ')
    search_query = beautify(original_search_query)
    movies = db_model.search_movies(search_query)
    actors = db_model.search_actors(search_query)

    movies = map(lambda x: (x[0], x[1].replace(' ', '-')), movies)
    actors = map(lambda x: (x[0], x[1].replace(' ', '-')), actors)

    context = {
        'search_query': original_search_query,
        'movies': list(movies),
        'actors': list(actors)
    }

    return context


def movie_detail(request, url_beautified):
    url_beautified = url_beautified.replace('-', ' ')
    movie, actors = db_model.get_movie(url_beautified)
    actors = map(lambda x: (x[0], x[1].replace(' ', '-')), actors)

    context = {
        'name': movie[1],
        'actors': list(actors)
    }
    return render(request, 'movie_detail.html', context=context)


def actor_detail(request, url_beautified):
    url_beautified = url_beautified.replace('-', ' ')
    actor, movies = db_model.get_actor(url_beautified)
    movies = map(lambda x: (x[0], x[1].replace(' ', '-')), movies)

    context = {
        'name': actor[1],
        'movies': list(movies)
    }
    return render(request, 'actor_detail.html', context=context)


def perform_scrape(request):
    populate(db_model)
    return HttpResponse("Scraping finished. All data are stored in database.")
