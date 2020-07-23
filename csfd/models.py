from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=70)
    name_beautified = models.CharField(max_length=70)
    link = models.CharField(max_length=255)


class Movie(models.Model):
    name = models.CharField(max_length=70)
    name_beautified = models.CharField(max_length=70)
    link = models.CharField(max_length=255)
    actors = models.ManyToManyField('Actor', through='ActorMovie')


class ActorMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
