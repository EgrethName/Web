from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Question, do_login
from .forms import AskForm, AnswerForm, SignupForm, SiteLoginForm
from django.shortcuts import render, get_object_or_404, redirect
import datetime


def main(request):
    ordered_questions = Question.objects.new()
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    user = request.user.username
    print(request, request.user)
    paginator = Paginator(ordered_questions, limit)
    paginator.baseurl = '/?page='
    paginator.limit = '&limit='
    page = paginator.page(page)
    return render(request, 'questions_by_date.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
        'user': user,
    })                                         


def popular(request):
    ordered_questions = Question.objects.popular()
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    paginator = Paginator(ordered_questions, limit)
    paginator.baseurl = '/popular/?page='
    page = paginator.page(page)
    return render(request, 'popular/questions_by_rating.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


def one_question(request, number):
    question = get_object_or_404(Question, id=number)
    if request.method == "POST":
        form = AnswerForm(request.user, question, request.POST)
        if form.is_valid():
            form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm()
    return render(request, 'question_details.html', {
        'form': form,
        'question': question,
        'author': question.author.username,
        'answers': question.answer_set.all(),
    })


def ask(request):
    if request.method == "POST":
        form = AskForm(request.user, request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask/add_question.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            sessionid = do_login(username, password)
            if sessionid:
                response = HttpResponseRedirect('/')
                response.set_cookie('sessionid', sessionid, httponly=True,
                                    expires=datetime.datetime.today() + datetime.timedelta(days=30)
                                    )
                return response
        return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})


def site_login(request):
    error = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        url = request.POST.get('continue', '/')
        sessionid = do_login(username, password)
        if sessionid:
            response = HttpResponseRedirect(url)
            response.set_cookie('sessionid', sessionid, httponly=True,
                                expires=datetime.datetime.today() + datetime.timedelta(days=30)
                                )
            return response
        else:
            error = u'Неверный логин/пароль'

    form = SiteLoginForm()
    return render(request, 'auth/login.html', {'form': form, 'error': error})
