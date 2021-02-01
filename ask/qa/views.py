from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from .models import Question
from django.shortcuts import render, get_object_or_404


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def main(request):
    ordered_questions = Question.objects.new()
    print('ordered_questions: {}'.format(ordered_questions))
    filtered_questions = ordered_questions.filter(is_published=True)
    print('filtered_questions: {}'.format(filtered_questions))

    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    paginator = Paginator(filtered_questions, limit)
    paginator.baseurl = '/?page='
    page = paginator.page(page)
    return render(request, 'questions_by_date.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


def popular(request):
    ordered_questions = Question.objects.popular()
    filtered_questions = ordered_questions.filter(is_published=True)
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    paginator = Paginator(filtered_questions, limit)
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
