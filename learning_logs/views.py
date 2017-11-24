# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.

def index(request):
    #homepage for learning log
    return render(request, 'learning_logs/index.html')

@login_required #decorator - will only open topics if user is logged on
def topics(request):
    #Show all topics
    topics = Topic.objects.filter(owner=request.user).order_by('date_added') #now you can only see your own topics
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required #decorator -
def topic(request, topic_id): #accepts value from the topic_id regex and stores it
    #show all topics
    topic = Topic.objects.get(id=topic_id) #get retrieves the topic

    # Make sure topic belongs to the user
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added') #lists entries by most recent
    context = {'topic':topic, 'entries':entries } #storing topics and entries in the context dict.
    return render(request, 'learning_logs/topic.html', context) # we send the context to topics.html

@login_required #decorator -
def new_topic(request): #Let users add their own content
    #Add new topic
    if request.method != 'POST': #if request method is get
        #No data submitted, create a new form
        form = TopicForm() #return blank form
    else: #if request method is post
        form = TopicForm(request.POST)#create form with user's data
        if form.is_valid(): #ensures all data has been entered, not over 200 char, etc
            form.save() #saves to database
            return HttpResponseRedirect(reverse('learning_logs:topics'))#redirects user to topics page

    context = {'form': form} #dict containing the get TopicForm
    return render(request, 'learning_logs/new_topic.html', context)

@login_required #decorator -
def new_entry(request, topic_id): #topic id finds the right topic
    #Add new entry for a topic
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST': #if request is get
        #No data, create a blank form
        form = EntryForm()
    else:
        #Post data submitted + process
        form = EntryForm(data=request.POST) #creates entry form with post data
        if form.is_valid():
            new_entry = form.save(commit=False) #don't save in database yet
            new_entry.owner = request.user #save topic as same from line 44
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))#redirects to topic page they made entry for

    context = {'topic':topic, 'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required #decorator -
def edit_entry(request, entry_id):
    #Edit an existing entry
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    # Make sure topic belongs to the user
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        #Post data submitted; process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args = [topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request,'learning_logs/edit_entry.html',context)


















