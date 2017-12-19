# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse

class QuestionsManager(models.Manager):
    def best_questions(self):
        return self.order_by("-rating")
    def tag_questions(self, tag):
        return self.filter(tags__tag=tag).all()

class AnswersManager(models.Manager):
    def question_aswers(self, qId):
        return self.filter(question = qId)


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/', default='uploads/avatar.jpg')
    rating = models.IntegerField(default=0, verbose_name=u"Рейтинг пользователя")
    def __unicode__(self):
        return self.username

class Tag(models.Model):
    tag = models.CharField(max_length=30)
    def __unicode__(self):
        return self.tag

class Question(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(verbose_name=u"Полное описание вопроса")
    createDate = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    author = models.ForeignKey(User, related_name="Q_author")
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0, verbose_name=u"Рейтинг вопроса")
    manager = QuestionsManager()
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ["-createDate"]

class Answer(models.Model):
    text = models.TextField(verbose_name=u"Текст ответа")
    createDate = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    author = models.ForeignKey(User)
    isCorrect = models.BooleanField(default=False, verbose_name=u"Правильность ответа")
    rating = models.IntegerField(default=0, verbose_name=u"Рейтинг ответа")
    question = models.ForeignKey(Question)
    manager = AnswersManager()
    def __unicode__(self):
        return self.text
    class Meta:
        ordering = ["-createDate"]

class LikeToQuestion(models.Model):
    who = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    isLike = models.BooleanField()

class LikeToAnswer(models.Model):
    who = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)
    isLike = models.BooleanField()