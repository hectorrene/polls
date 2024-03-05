from django.http import HttpResponse
from django.urls import path, reverse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404 , HttpResponse , HttpResponseRedirect
from django.views import generic 
from django.utils import timezone
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from . import views
from django.contrib.auth.views import LoginView
from .models import Choice, Question 
from .forms import new_questionForm, updateQuestionForm

def home (request) :
    return render (request, 'polls/home.html')

def menu (request) :
    return render (request, 'polls/menu.html' )

class QuestionListView(generic.ListView):
    model = Question
    template_name = "polls/question_list.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:30]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/question_detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/question_results.html"

class MenuView(generic.ListView):
    model = Question
    template_name = 'polls/menu.html'
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:30]

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

class new_questionFormView (FormView):
    template_name = "menu.html"
    form_class = new_questionForm
    success_url = "/thanks/"

    def form_valid(self, form):
        form.save_question()
        return super().form_valid(form)

class UpdateQuestion (UpdateView, PermissionRequiredMixin ) :
    model = Question 
    template_name = 'polls/update_question.html'
    fields = ['pub_date', 'question_text']
    success_url = reverse_lazy('polls:menu')

class UpdateChoice (UpdateView, PermissionRequiredMixin):
    model = Choice
    template_name = 'polls/update_choice.html'
    fields = ['choice_text', 'votes']
    success_url = reverse_lazy ('polls:menu')

class CreateQuestion (CreateView, PermissionRequiredMixin) :
    model = Question 
    template_name = 'polls/create_question.html'
    fields = ['pub_date', 'question_text']
    success_url = reverse_lazy('polls:menu')

    def get_initial(self):
        return {'pub_date': timezone.now()}

    def form_valid (self, form) :
        form.instance.pub_date = timezone.now()
        return super().form_valid(form)
    
class CreateChoice (CreateView, PermissionRequiredMixin) :
    model = Choice
    template_name = 'polls/create_choice.html'
    fields = ['question', 'choice_text', 'votes']
    success_url = reverse_lazy('polls:menu')

class DeleteQuestion (DeleteView, PermissionRequiredMixin) :
    model = Question 
    template_name = 'polls/delete_question.html'
    fields = ['pub_date', 'question_text']
    success_url = reverse_lazy('polls:menu')

class DeleteChoice (DeleteView, PermissionRequiredMixin) :
    model = Choice
    template_name = 'polls/delete_choice.html'
    fields = ['question', 'choice_text', 'votes']
    success_url = reverse_lazy('polls:menu')