from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from .models import Question
from .models import QuestionManager
from .models import Answer
from django.shortcuts import render, get_object_or_404


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def main(request):
    questions = Question.objects.filter(is_published=True)
    questions = QuestionManager.new(questions)
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    paginator = Paginator(questions, limit)
    paginator.baseurl = '/?page='
    page = paginator.page(page)
    return render(request, 'questions_by_date.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


def popular(request):
    questions = Question.objects.filter(is_published=True).popular()
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    paginator = Paginator(questions, limit)
    paginator.baseurl = '/popular/?page='
    page = paginator.page(page)
    return render(request, 'popular/questions_by_rating.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


@require_GET
def one_question(request, number):
    question = get_object_or_404(Question, id=number)
    return render(request, 'question_details.html', {
        'question': question,
        'answers': question.answer_set.all(),
    })
