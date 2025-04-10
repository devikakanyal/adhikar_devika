from django.db import models
from django.contrib.auth.models import User
# from django.db import models
from django.utils import timezone

class FIR(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    ipfs_hash = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f'Comment by {self.author}'



class Lawyer(models.Model):
    TYPE_CHOICES = [
        ('NGO', 'Non-Governmental Organization'),
        ('Non-Profit', 'Non-Profit'),
        ('Profit', 'Private Firm / Individual'),
    ]

    name = models.CharField(max_length=255)
    lawyer_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=15)
    rating = models.FloatField(default=0.0)
    verified = models.BooleanField(default=False)

    def _str_(self):
        return self.name        