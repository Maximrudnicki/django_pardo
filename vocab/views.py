from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Word


class WordList(ListView):
    model = Word
    context_object_name='vocab'
    template_name = 'vocab/vocab.html'


class WordDetail(DetailView):
    model = Word
    context_object_name = 'word'


class WordCreate(CreateView):
    model = Word
    fields = ('word', 'definition', 'learned')
    success_url = reverse_lazy('vocab')


class WordUpdate(UpdateView):
    model = Word
    fields = ('word', 'definition', 'learned')
    success_url = reverse_lazy('vocab')


class WordDelete(DeleteView):
    model = Word
    context_object_name = 'word'
    success_url = reverse_lazy('vocab')
