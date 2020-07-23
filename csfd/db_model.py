import sqlite3
from typing import Dict, List
from csfd.models import Actor, Movie, ActorMovie


class DBModel:

    def __init__(self):
        self._connect()

    def _connect(self):
        self.conn = sqlite3.connect('db.sqlite3')

    def clear_db(self):
        Movie.objects.all().delete()
        Actor.objects.all().delete()

    def insert_movies_to_db(self, movies: List[Dict[str, str]]):
        Movie.objects.bulk_create([Movie(**{'name': movie['name'],
                                            'name_beautified': movie['beautified'],
                                            'link': movie['link']})
                                   for movie in movies])

        return Movie.objects.all()

    def link_actors_to_movies(self, movie, actors):
        ActorMovie.objects.bulk_create([ActorMovie(**{'movie': movie,
                                                      'actor': actor,
                                                      'order': i})
                                        for i, actor in enumerate(actors)])

    def insert_actors_to_db(self, actors):
        actors_to_create = []
        actors_created = set()  # Do not resolve uniqueness for now
        for actor in actors:
            db_actor = Actor.objects.filter(name_beautified=actor['beautified'])
            if not db_actor and actor['beautified'] not in actors_created:
                actors_to_create += [actor]
                actors_created.add(actor['beautified'])

        Actor.objects.bulk_create([Actor(**{'name': actor['name'],
                                            'name_beautified': actor['beautified'],
                                            'link': actor['link']})
                                   for actor in actors_to_create])

        actors_all = []
        for actor in actors:
            actors_all += [Actor.objects.get(name_beautified=actor['beautified'])]

        return actors_all

    def search_movies(self, search_query):
        return Movie.objects.filter(name_beautified__contains=search_query)

    def search_actors(self, search_query):
        return Actor.objects.filter(name_beautified__contains=search_query)

    def get_movie(self, beautified):
        return Movie.objects.get(name_beautified=beautified)

    def get_actor(self, beautified):
        return Actor.objects.get(name_beautified=beautified)
