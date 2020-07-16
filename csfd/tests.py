from django.test import TestCase
import os

from csfd.views import beautify
import csfd.views

from csfd.model import DBModel
from csfd.custom_connection import CustomConnection

TEST_FILE = "test.sqlite3"


class ViewTestCase(TestCase):
    def setUp(self) -> None:
        conn = CustomConnection(TEST_FILE)
        self.db_model = DBModel(conn=conn)
        self.db_model.create_structure()

        movies = [
            {'name': 'Forrest Gump', 'beautified': beautify('Forrest Gump'), 'link': '', 'actors': ['tom hanks']},
            {'name': 'Zelená míle', 'beautified': beautify('Zelená míle'), 'link': '', 'actors': ['tom hanks']},
            {'name': 'Terminátor 2: Den zúčtování', 'beautified': beautify('Terminátor 2: Den zúčtování'),
             'link': '', 'actors': ['arnold schwarzenegger']},
        ]

        self.db_model.insert_movies_to_db(movies)

        actors = {beautify('Tom Hanks'):
                  {'name': 'Tom Hanks', 'beautified': beautify('Tom Hanks'), 'link': ''},
                  beautify('Arnold Schwarzenegger'):
                  {'name': 'Arnold Schwarzenegger', 'beautified': beautify('Arnold Schwarzenegger'), 'link': ''}
        }

        for movie in movies:
            self.db_model.insert_actors_to_db(movie['db_id'], movie['actors'], actors)

    def tearDown(self) -> None:
        os.unlink(TEST_FILE)

    def test_search_for(self) -> None:
        csfd.views.db_model = self.db_model
        context = csfd.views._search_for('forrest gump')

        self.assertEqual(context['search_query'], 'forrest gump')
        self.assertEqual(len(context['movies']), 1)
        self.assertEqual(context['movies'][0], ('Forrest Gump', 'forrest-gump'))
