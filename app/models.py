from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here


class User(AbstractUser):

    user = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(null=True , blank=True)
    image = models.ImageField(upload_to='profile_images')

    REQUIRED_FIELDS = []



class Feedback(models.Model):
    Feedback_Choices = (
        ('good', 'Good'),
        ('bad', 'Bad'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=100)
    good_or_bad = models.CharField(max_length=100, choices=Feedback_Choices)
    
    
    def __str__(self):
        return self.feedback


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.TextField()
    link = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='projects')
    no_of_likes = models.IntegerField(default=0)
 

    
    def __str__(self):
        return self.name


        
class LikeProject(models.Model):
    project_id = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    


class Community(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    image = models.ImageField(upload_to='community', null=True, blank=True)
    no_of_comments = models.IntegerField(default=0)

    
    def __str__(self):
        return self.question


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community,  on_delete=models.CASCADE)
    body = models.TextField(default='add comment')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
    