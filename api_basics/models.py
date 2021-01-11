from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=100)
    date_posted=models.DateTimeField(default=timezone.now)
    email=models.EmailField(max_length=100)
    content=models.TextField()

    def __str__(self):
        return self.title
    