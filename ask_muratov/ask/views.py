# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from ask.models import User, Tag, Question, Answer, LikeToAnswer, LikeToQuestion
from ask.forms import *
from django.core.urlresolvers import reverse
from faker import Faker
from random import randint

def mainPage(request):
    #setup()
    qlist = Question.manager.all()
    questions = paginate(request, qlist, 10)
    return render(request, 'questions.html', {
        'title': 'New questions',
        'questions': questions,
        'linkName': 'Hot questions',
        'link': reverse('hotQuestions'),
    })

def hotQuestions(request):
    qlist = Question.manager.best_questions()
    questions = paginate(request, qlist, 10)
    return render(request, 'questions.html', {
        'title': 'HotQuestions',
        'questions': questions,
        'linkName': 'New questions',
        'link': reverse('mainPage'),
    })

@require_GET
def tagQuestions(request, tag):
    qlist = Question.manager.tag_questions(tag)
    questions = paginate(request, qlist, 10)
    return render(request, 'questions.html', {
        'title': 'Tag:' + tag ,
        'caption': 'Tag: ' + tag,
        'questions': questions,
        'linkName': '',
        'link': '',
    })


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answ = Answer.manager.question_aswers(question_id)
    answers = paginate(request, answ.values(), 10)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save(question, request.user)
            return HttpResponseRedirect(reverse('question', kwargs={'question_id': question.pk}))
    else:
        form = AnswerForm()
    return render(request, 'question.html', {
        'title': 'Question',
        'question': question,
        'answers': answers,
        'form': form,
    })

def loginPage(request):
    redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(redirect)
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'title': 'Login',
        'form': form,
    })

def registerPage(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {
        'title': 'Signup',
        'form': form,
    })

@login_required(redirect_field_name='continue')
def askQuestion(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(request.user, 0)
            return HttpResponseRedirect(reverse('question', kwargs={'id': q.id}))
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {
        'title': 'Ask',
        'form': form,
     })

@login_required(redirect_field_name='continue')
def settings(request):
    user = USERS.get('1')
    return render(request, 'settings.html', {
        'title': 'Settings',
        'user': user
    })

@login_required(redirect_field_name='continue')
def logout(request):
	redirect = request.GET.get('continue', '/')
	auth.logout(request)
	return HttpResponseRedirect(redirect)


def paginate(request, objList, objOnPage):
    page = request.GET.get('page')
    paginator = Paginator(objList, objOnPage)
    try:
        elements = paginator.page(page)
    except PageNotAnInteger:
        elements = paginator.page(1)
    except EmptyPage:
        elements = paginator.page(paginator.num_pages)
    return elements

def setup():
    f = Faker()
    tags = f.words(nb=20)
    for i in tags:
        a = Tag(tag=i)
        a.save()

    for i in range(100):
        tt = f.text(50)
        te = f.text()
        a = Question(title=tt, text=te, author_id=randint(2,4))
        a.save()
        a.tags.add(randint(1,20),randint(1,20),randint(1,20))

    for i in range(300):
        te = f.text()
        an = Answer(text=te, author_id=randint(2,4), question_id=randint(1,100))
        an.save()


