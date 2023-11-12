from django.shortcuts import render, redirect, get_object_or_404
from .models import Poll, Answer, Vote
from django.forms import modelformset_factory
from django.http import HttpResponse
import random

def index(request):
    polls = Poll.objects.all()
    if polls.count() > 5:
        polls = random.sample(list(polls), 5)
    else:
        polls = list(polls)
    context = {'polls': polls}
    return render(request, 'index.html', context=context)

def create_poll(request):
    AnswerFormSet = modelformset_factory(Answer, fields=('answer',), extra=2, max_num=10)
    if request.method == 'POST':
        formset = AnswerFormSet(request.POST)
        if formset.is_valid():
            poll = Poll(question=request.POST.get('question'))
            poll.save()
            for form in formset:
                answer = form.save(commit=False)
                answer.poll = poll
                answer.save()
            return redirect('vote_poll', poll.id)  # Redirect to the index page or another appropriate page
    else:
        formset = AnswerFormSet(queryset=Answer.objects.none())
    return render(request, 'create_poll.html', {'formset': formset})

def vote_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    session_key = request.session.session_key
    if Vote.objects.filter(poll=poll, session_key=session_key).exists():
            return redirect('results', poll_id=poll.id)
    if request.method == 'POST':      
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        # Process vote
        answer_id = request.POST.get('answer')
        answer = Answer.objects.get(id=answer_id)
        answer.votes += 1
        answer.save()

        # Record the user's vote
        Vote.objects.create(poll=poll, session_key=session_key)
        
        return redirect('results', poll_id=poll.id)  # Redirect to a results page or similar
    else:
        # Show the poll voting form
        return render(request, 'vote_poll.html', {'poll': poll})
    
def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':      
        return redirect('index')
    return render(request, 'results.html', {'poll': poll})
