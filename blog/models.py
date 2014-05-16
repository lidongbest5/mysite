from django.db import models
import datetime

class Blog(models.Model):
    title = models.CharField(max_length=120,blank=True)
    content = models.TextField()
    date = models.DateField('datepublished',blank=True,default=datetime.datetime.now().date())
    category = models.CharField(max_length=30)
    img = models.CharField(max_length=100,blank=True,null=True)
    def __unicode__(self):
        return self.title

class Comment(models.Model):
    blogid = models.IntegerField()
    content = models.TextField()
    date = models.DateField('datepublished',blank=True,default=datetime.datetime.now().date())
    name = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(null=True)
    def __unicode__(self):
        return self.content

class Message(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    message = models.TextField()
    def __unicode__(self):
        return self.name

class Saying(models.Model):
    name = models.CharField(max_length=32,default='Lidong')
    avatar = models.CharField(max_length=64,default='/static/images/head.png')
    place = models.CharField(max_length=120,blank=True)
    content = models.TextField()
    img = models.CharField(max_length=256,blank=True,null=True)
    date = models.DateTimeField(blank=True,default=datetime.datetime.now())
    favourite = models.IntegerField(default=0)
    video = models.CharField(max_length=256,blank=True,null=True)
    audio = models.CharField(max_length=256,blank=True,null=True)
    def __unicode__(self):
        return self.content

class SayingComment(models.Model):
    SayingId = models.IntegerField()
    name = models.CharField(max_length=20,blank=True,null=True)
    content = models.TextField()
    date = models.DateTimeField(blank=True,default=datetime.datetime.now())
    def __unicode__(self):
        return self.content

class SayingFavourite(models.Model):
    num = models.IntegerField(default=0)
    def __unicode__(self):
        return self.num 

class Account(models.Model):
    dong = models.IntegerField(default=0)
    yang = models.IntegerField(default=0)
    he = models.IntegerField(default=0)
    han = models.IntegerField(default=0)

class AccountDetail(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now())
    num = models.IntegerField()
    content = models.TextField()
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=32)
