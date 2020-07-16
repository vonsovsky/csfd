from typing import Dict, List, Tuple
from django.db import connection


class DBModel:

    def __init__(self, conn=connection):
        self._connection = conn

    def insert_movies_to_db(self, movies: Dict[str, str]):
        with self._connection.cursor() as cursor:
            for movie in movies:
                query = "INSERT INTO movies (name, name_beautified, link) VALUES (\"{}\", \"{}\", \"{}\")" \
                    .format(movie['name'], movie['beautified'], movie['link'])
                cursor.execute(query)
                movie['db_id'] = cursor.lastrowid

    def insert_actors_to_db(self, movie_id: int, actors_list: List[str], actors: Dict[str, str]):
        """
        Inserts movie actors into db if they don't exist there yet and stores their insertion id into `actors` dict
        Inserts all movie actors into many to many relationship with movies
        """

        with self._connection.cursor() as cursor:
            for actor_name in actors_list:
                actor = actors[actor_name]
                if 'db_id' not in actor:
                    query = "INSERT INTO actors (name, name_beautified, link) VALUES (\"{}\", \"{}\", \"{}\")" \
                        .format(actor['name'], actor['beautified'], actor['link'])
                    cursor.execute(query)
                    actor['db_id'] = cursor.lastrowid

                query = "INSERT INTO movie_actors (movie, actor) VALUES ({}, {})" \
                    .format(movie_id, actor['db_id'])
                cursor.execute(query)

    def search_movies(self, search_query: str) -> List[Tuple[str, str]]:
        return self.search_objects('movies', search_query)

    def search_actors(self, search_query: str) -> List[Tuple[str, str]]:
        return self.search_objects('actors', search_query)

    def search_objects(self, obj_name: str, search_query: str) -> List[Tuple[str, str]]:
        with self._connection.cursor() as cursor:
            query = "SELECT name, name_beautified FROM {} WHERE name_beautified LIKE '%{}%'"\
                .format(obj_name, search_query)
            cursor.execute(query)
            return cursor.fetchall()

    def get_movie(self, beautified: str):
        return self.get_object(
            'movies',
            'SELECT A.name, A.name_beautified FROM movie_actors MA ' +
            'INNER JOIN actors A ON A.id = MA.actor WHERE MA.movie = {}',
            beautified
        )

    def get_actor(self, beautified: str):
        return self.get_object(
            'actors',
            'SELECT M.name, M.name_beautified FROM movie_actors MA ' +
            'INNER JOIN movies M ON M.id = MA.movie WHERE MA.actor = {}',
            beautified
        )

    def get_object(self, obj_name: str, ref_query: str, beautified: str) -> Tuple[Tuple[int, str], List[Tuple[str, str]]]:
        with self._connection.cursor() as cursor:
            query = "SELECT id, name FROM {} WHERE name_beautified = '{}'".format(obj_name, beautified)
            cursor.execute(query)
            obj = cursor.fetchone()

            cursor.execute(ref_query.format(obj[0]))
            results = cursor.fetchall()

        return obj, results

    def create_structure(self):
        """
        Used for testing
        """

        sql_create_actors = """CREATE TABLE IF NOT EXISTS "actors" (
            "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "name"  TEXT,
            "name_beautified"  TEXT,
            "link"  TEXT
            );"""

        sql_create_movies = """CREATE TABLE IF NOT EXISTS "movies" (
            "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "name"  TEXT,
            "name_beautified"  TEXT,
            "link"  TEXT
            );"""

        sql_create_many_to_many = """CREATE TABLE IF NOT EXISTS "movie_actors" (
            "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "movie"  INTEGER NOT NULL,
            "actor"  INTEGER NOT NULL,
            CONSTRAINT "movie_id" FOREIGN KEY ("movie") REFERENCES "movies" ("id"),
            CONSTRAINT "actor_id" FOREIGN KEY ("actor") REFERENCES "actors" ("id")
            );"""

        with self._connection.cursor() as cursor:
            cursor.execute(sql_create_actors)
            cursor.execute(sql_create_movies)
            cursor.execute(sql_create_many_to_many)