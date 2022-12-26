from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    nickname = models.CharField(blank=True, null=True, max_length=20)
    email = models.EmailField(blank=True, null=True)
    avatar = models.FileField(upload_to='avatar/')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True, null=True)
    subscribe = models.BooleanField(default=False)


    class Meta:
        db_table = "v_user"

class Feedback(models.Model):
    contact = models.CharField(blank=True, null=True, max_length=20)
    content = models.CharField(blank=True, null=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "v_feedback"