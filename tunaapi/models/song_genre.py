from django.db import models
from .song import Song
from .genre import Genre

class SongGenre(models.Model):
    """Model that represents the relationship between song and its genres"""
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
