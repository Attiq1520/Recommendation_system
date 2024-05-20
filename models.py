# recommendations/models.py
from django.db import models

class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)
    plot = models.TextField()
    director = models.CharField(max_length=255)
    actors = models.TextField()
    poster_url = models.URLField()
