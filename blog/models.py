from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Get the user model for referencing authors
User = get_user_model()

class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the user who authored the post
    favorites = models.ManyToManyField(User, related_name="favorite_posts", blank=True)  # Users who favorited this post

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL to access a detail view of this post.
        """
        return reverse('post-detail', kwargs={'pk': self.pk})


class Announcement(models.Model):
    """
    Model representing an announcement.
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    """
    Model representing an event with a name, date, and location.
    """
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
