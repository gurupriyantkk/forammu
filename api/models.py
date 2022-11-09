from distutils.command.upload import upload
from email.mime import image
from enum import auto
from re import T
from turtle import title
from unittest.util import _MAX_LENGTH
from django.db import models 
from django.contrib.auth.models import User

# Create your models here.

class Questions(models.Model):
    title=models.CharField(max_length=250)
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images",null=True)
    created_date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    @property
    def question_answers(self):
        return self.answers_set.all()

    def __str__(self):
        return self.title

class Answers(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    upvote=models.ManyToManyField(User,related_name="upvote")
    created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.answer
