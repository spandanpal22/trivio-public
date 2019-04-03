from django.db import models
import os
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


def default_score():
    return 0

def default_interval():
    return 10
class CustomUser(AbstractUser):
    user_name = models.CharField(blank=False, max_length=255)
    name = models.CharField(blank=False, max_length=255)
    score=models.IntegerField(default=default_score())
    college=models.CharField(max_length=60,blank=False,null=False)
    status=models.IntegerField(default=0,blank=False)
    flag=models.IntegerField(default=0,blank=False)
    email_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def publish(self):
        self.save()
@receiver(post_save, sender=AbstractUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(CustomUser=instance)
    instance.CustomUser.save()

class Question(models.Model):
    question=models.CharField(max_length=300)
    answer=models.CharField(max_length=50,blank=False)
    option1=models.CharField(max_length=50,blank=False)
    option2=models.CharField(max_length=50,blank=False)
    option3=models.CharField(max_length=50,blank=False)
    option4=models.CharField(max_length=50,blank=False)
    def publish(self):
        self.save()

    def __str__(self):
        return self.question


class Event(models.Model):
    Event_name=models.CharField(default="trivio",max_length=50,blank=False)
    event_start=models.DateTimeField(auto_now_add=False)
    interval=models.IntegerField(default=default_interval())