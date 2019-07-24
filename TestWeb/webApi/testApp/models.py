# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# class Topic(models.Model): 
#     """用户学习的主题"""
#     text = models.CharField(max_length=200)
#     date_added = models.DateTimeField(auto_now_add=True)
    
#     def __unicode__(self): 
#         """返回模型的字符串表示"""
#         return self.text
# class Entry(models.Model): 
#     """学到的有关某个主题的具体知识"""
#     topic = models.ForeignKey(Topic)
#     text = models.TextField()
#     date_added = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         verbose_name_plural = 'entries'
#         def __str__(self):
#             """返回模型的字符串表示"""
#             return self.text[:50] + "..."
        

from django.contrib.auth.models import User

class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text

class Entry(models.Model):
    """Something specific learned about a topic."""
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'
 
    def __str__(self):
        """Return a string representation of the model."""
        return self.text[:50] + "..."