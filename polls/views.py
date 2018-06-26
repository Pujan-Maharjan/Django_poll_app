from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
# from django.template import loader
from django.urls import reverse
from django.db.models import F
from .models import Question, Choice

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    context = {
        'latest_question_list': latest_question_list
    }

    template = 'polls/index.html'

    return render(request, template, context)


def detail(request, question_id):

    try:

        question = Question.objects.get(pk = question_id) #question = get_object_or_404(Question, pk=question_id)
        choices = question.choice_set.all()
    except Question.DoesNotExist:
        raise Http404("Question Does Not Exists")

    return render(request,'polls/detail.html', {'question':question, 'choices':choices})

def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/results.html', { 'question':question})



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




