from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    goodreads_id = models.IntegerField(unique=True)  # For matching with Goodreads dataset
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.FloatField()  # Scale 1-5
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # Prevent duplicate ratings