from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from ask.views import *

urlpatterns = [
    url(r'^$', mainPage, name = 'mainPage'),
    url(r'^hot/$', hotQuestions, name = 'hotQuestions'),
    url(r'^tag/(?P<tag>\w+)/$', tagQuestions, name = 'tagQuestions'),
    url(r'^question/(?P<question_id>[0-9]+)/$', question, name = 'question'),
    url(r'^login/$', loginPage, name = 'loginPage'),
    url(r'^signup/$', registerPage, name = 'registerPage'),
    url(r'^ask/$', askQuestion, name = 'askQuestion'),
    url(r'^settings/$', settings, name = 'settings'),
    url(r'^logout/$', logout, name = 'logout'),
]
urlpatterns += staticfiles_urlpatterns()