from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=70)
    name_beautified = models.CharField(max_length=70)
    link = models.CharField(max_length=255)
    movies = models.ManyToManyField('Movie')


class Movie(models.Model):
    name = models.CharField(max_length=70)
    name_beautified = models.CharField(max_length=70)
    link = models.CharField(max_length=255)
