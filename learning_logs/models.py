# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    #Topic the user is learning about
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User) #Topic is the most central data in site, so we can connect the topic/entry to the user

    def __str__(self):
        #returns a str representation of the model
        return self.text

class Entry(models.Model):
    #Something learned about a topic
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        #Returns str representation of the model
        return self.text[:50]+'...'