from django.urls import path
from .views import (
    WordListView,
    WordDetailView,
    WordCreateView,
    WordUpdateView,
    WordDeleteView,
    WordSearchView,
)

urlpatterns = [
    path('', WordListView.as_view(), name='vocab'),
    path('<int:pk>/', WordDetailView.as_view(), name='word'),
    path('word-create/', WordCreateView.as_view(), name='word-create'),
    path('word-update/<int:pk>/', WordUpdateView.as_view(), name='word-update'),
    path('word-delete/<int:pk>/', WordDeleteView.as_view(), name='word-delete'),
    path('search/', WordSearchView.as_view(), name='word-search'),
]