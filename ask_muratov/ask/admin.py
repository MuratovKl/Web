# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ask.models import Question, User, Answer

admin.site.register(Question)
admin.site.register(User, UserAdmin)
admin.site.register(Answer)