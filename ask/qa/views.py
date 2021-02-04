from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from .models import Question, Answer
from .forms import AskForm
from .forms import AnswerForm
from django.shortcuts import render, get_object_or_404, redirect


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def main(request):
    ordered_questions = Question.objects.new()
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    paginator = Paginator(ordered_questions, limit)
    paginator.baseurl = '/?page='
    page = paginator.page(page)
    return render(request, 'questions_by_date.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
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
        form = AnswerForm(question, request.POST)
        if form.is_valid():
            form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm()
    return render(request, 'question_details.html', {
        'form': form,
        'question': question,
        'answers': question.answer_set.all(),
    })


def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask/add_question.html', {'form': form})

