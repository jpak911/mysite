# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from . import models


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self, pub_date__lte=None):
        return models.Question.objects.filter(
            pub_date__lte - timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = models.Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = models.Question
    template_name = 'polls/results.html'


def detail(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def index(request):
    latest_question_list = models.Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def results(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, models.Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error message': "You didn't make a Choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
