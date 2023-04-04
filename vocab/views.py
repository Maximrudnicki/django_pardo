from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Word
from .mixins import WordAccessMixin


class WordListView(WordAccessMixin, ListView):
    model = Word
    context_object_name = 'vocab'
    template_name = 'vocab/vocab.html'


class WordSearchView(WordAccessMixin, ListView):
    context_object_name = 'vocab'
    template_name = 'vocab/word_search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Word.objects.by_user(self.request.user).filter(word__icontains=query)
        else:
            return Word.objects.none()


class WordDetailView(WordAccessMixin, DetailView):  
    model = Word
    context_object_name = 'word'


class WordCreateView(WordAccessMixin, CreateView):
    model = Word
    fields = ('word', 'definition', 'learned')
    success_url = reverse_lazy('vocab')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WordUpdateView(WordAccessMixin, UpdateView):
    model = Word
    fields = ('word', 'definition', 'learned')
    success_url = reverse_lazy('vocab')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WordDeleteView(WordAccessMixin, DeleteView):
    model = Word
    context_object_name = 'word'
    success_url = reverse_lazy('vocab')
