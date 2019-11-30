from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import Choice, Question

import logging

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def index(request):
    return HttpResponseRedirect(reverse("polls:index"))


def configure():
    """Configure loggers and log handlers"""
    filehandler = logging.FileHandler("demo.log")
    filehandler.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    filehandler.setFormatter(formatter)

    root = logging.getLogger()
    root.addHandler(filehandler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(fmt='%(levelname)-8s %(name)s: %(message)s')
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

class EyesOnlyView(LoginRequiredMixin, generic.ListView):
    # this is the default. Same default as in auth_required decorator
    login_url = '/accounts/login/'

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        configure()
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        configure()
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    configure()

@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Vote for one of the answers to a question."""
    user = request.user
    print("current user is", user.id, "login", user.username)
    print("Real name:", user.first_name, user.last_name)
    question = get_object_or_404(Question, pk=question_id)
    try:
        configure()
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        configure()
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        configure()
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))