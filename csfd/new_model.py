"""
WIP: file is not being used yet
"""

import sqlite3
from typing import Dict, Union, List
from django.db import connection
from models.movies import Movies


class DBModel:

    def __init__(self):
        self._connect()

    def _connect(self):
        self.conn = sqlite3.connect('db.sqlite3')

    def insert_movies_to_db(self, movies):
        Movies.objects.bulk_create([Movies(**{'name': movie['name'],
                                              'name_beautified': movie['beautified'],
                                              'link': movie['link']})
                                    for movie in movies])

        for movie in movies:
            Movies.objects.create(name=movie['name'], name_beautified=movie['beautified'], link=movie['link'])

    # Dict[Union[str, List[int]]]
    def insert_actors_to_db(self, actors):
        with connection.cursor() as cursor:
            for _, actor in actors.items():
                query = "INSERT INTO actors (name, name_beautified, link) VALUES (\"{}\", \"{}\", \"{}\")" \
                    .format(actor['name'], actor['beautified'], actor['link'])
                cursor.execute(query)
                actor_id = cursor.lastrowid
                for movie_id in actor['movies']:
                    query = "INSERT INTO movie_actors (movie, actor) VALUES ({}, {})".format(movie_id, actor_id)
                    cursor.execute(query)

            self.conn.commit()

    def search_movies(self, search_query):
        return self.search_objects('movies', search_query)

    def search_actors(self, search_query):
        return self.search_objects('actors', search_query)

    def search_objects(self, obj_name, search_query):
        with connection.cursor() as cursor:
            query = "SELECT name, name_beautified FROM {} WHERE name_beautified LIKE '%{}%'"\
                .format(obj_name, search_query)
            cursor.execute(query)
            return cursor.fetchall()

    def get_movie(self, beautified):
        return self.get_object(
            'movies',
            'SELECT A.name, A.name_beautified FROM movie_actors MA ' +
            'INNER JOIN actors A ON A.id = MA.actor WHERE MA.movie = {}',
            beautified
        )

    def get_actor(self, beautified):
        return self.get_object(
            'actors',
            'SELECT M.name, M.name_beautified FROM movie_actors MA ' +
            'INNER JOIN movies M ON M.id = MA.movie WHERE MA.actor = {}',
            beautified
        )

    def get_object(self, obj_name, ref_query, beautified):
        with connection.cursor() as cursor:
            query = "SELECT id, name FROM {} WHERE name_beautified = '{}'".format(obj_name, beautified)
            cursor.execute(query)
            obj = cursor.fetchone()

            cursor.execute(ref_query.format(obj[0]))
            results = cursor.fetchall()

        return obj, results
