from django.db import models

class Genre(models.Model):
    """Model that represents a genre"""
    description = models.CharField(max_length=50)
