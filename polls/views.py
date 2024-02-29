from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import QuestionForm, ChoiceFormSet

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


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


def add_poll(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)

        if question_form.is_valid() and choice_formset.is_valid():
            question = question_form.save(commit=False)
            question.pub_date = timezone.now()
            question.save()
            choice_formset.instance = question
            choice_formset.save()
            return redirect('polls:index')
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet()

    return render(request, 'polls/add_poll.html', {
        'question_form': question_form,
        'choice_formset': choice_formset,
    })
