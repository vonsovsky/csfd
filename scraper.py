import os
from typing import List, Dict

import django
import requests
from bs4 import BeautifulSoup
from csfd.string_helper import beautify

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
URL_PREFIX = 'http://csfd.cz'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "csfd.settings")
django.setup()

from csfd.db_model import DBModel


def get_movies() -> List[Dict[str, str]]:
    movies = []
    url = 'https://www.csfd.cz/zebricky/nejlepsi-filmy/?show=complete'
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    div = soup.find(id="results")
    tds = div.findAll(class_='film')
    for td in tds:
        tag = td.find("a")
        link = URL_PREFIX + tag["href"]
        movie_name = tag.contents[0]
        movies.append({'name': movie_name, 'beautified': beautify(movie_name), 'link': link})

    return movies


def get_actors_for_movie(url: str) -> List[str]:
    movie_actors_list = []
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    div = soup.find(class_="creators")
    h4 = div.find("h4", string="Hrají:")
    actors_list = h4.parent.find('span').findAll('a')
    for actor in actors_list:
        actor_name = actor.contents[0]
        beautified = beautify(actor_name)
        link = URL_PREFIX + actor['href']

        movie_actors_list += [{'name': actor_name, 'beautified': beautified, 'link': link}]

    return movie_actors_list


if __name__ == "__main__":
    db_model = DBModel()
    db_model.clear_db()
    movies = get_movies()
    movies = db_model.insert_movies_to_db(movies)
    for i, movie in enumerate(movies):
        print("{}: Getting actors for {}".format(i + 1, movie.name))
        actors_list = get_actors_for_movie(movie.link)
        actors = db_model.insert_actors_to_db(actors_list)
        db_model.link_actors_to_movies(movie, actors)
