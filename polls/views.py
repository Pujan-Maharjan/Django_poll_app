import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
# from django.template import loader
from django.urls import reverse
from django.db.models import F
from django.utils import timezone
from django.views import generic
from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""

        return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    context_object_name = 'question'
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Return questions by excluding the future questions"""
        return Question.objects.exclude(pub_date__gt = timezone.now())
 
class ResultsView(generic.DetailView):
    model = Question
    template_name  = 'polls/results.html'



def vote(request, question_id):

    question = Question.objects.get(pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #redisplay the question from voting along with error message

        return render(request,'polls/detail.html', {
            'question':question,
            'choices':question.choice_set.all(),
            'error_message':"Please select a choice and submit"
        })

    else:
        selected_choice.votes=F('votes')+1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))




