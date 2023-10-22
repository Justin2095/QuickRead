from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    about = models.TextField(blank=True)

    #  profile_image =

    def __str__(self):
        return self.user.username


class Subject(models.Model):
    user = models.ForeignKey(Profile, default=None, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hours_per_week = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name


class Article(models.Model):
    subject = models.ManyToManyField(Subject)
    article_title = models.CharField(max_length=120)
    article_author = models.CharField(max_length=120)
    article_summary = models.TextField(null=True)
    article_content = models.TextField(null=True)

    def __str__(self):
        return self.article_title


class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Note(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class Flashcard(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.CharField(max_length=100)
    definition = models.TextField()

    def __str__(self):
        return self.term
