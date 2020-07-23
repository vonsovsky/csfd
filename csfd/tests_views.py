from django.test import TestCase

import csfd.views
from csfd.models import Movie, Actor
from csfd.string_helper import beautify


class ViewTestCase(TestCase):
    def setUp(self):
        actor1 = Actor.objects.create(name="Tom Hanks", name_beautified=beautify('Tom Hanks'), link='')
        actor2 = Actor.objects.create(name="Arnold Schwarzenegger", name_beautified=beautify('arnold schwarzenegger'),
                                      link='')

        movie1 = Movie.objects.create(name="Forrest Gump", name_beautified=beautify('Forrest Gump'), link='')
        movie2 = Movie.objects.create(name="Zelená míle", name_beautified=beautify('Zelená míle'), link='')
        movie3 = Movie.objects.create(name="Terminátor 2: Den zúčtování",
                                      name_beautified=beautify('Terminátor 2: Den zúčtování'), link='')

        movie1.actors.add(actor1)
        movie2.actors.add(actor1)
        movie3.actors.add(actor2)

    def test_search_for(self) -> None:
        context = csfd.views._search_for('forrest gump')

        self.assertEqual(context['search_query'], 'forrest gump')
        self.assertEqual(len(context['movies']), 1)
        self.assertEqual(context['movies'][0], {'name': 'Forrest Gump', 'name_beautified': 'forrest-gump'})
