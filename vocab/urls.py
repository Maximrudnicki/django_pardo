from django.urls import path
from .views import (
    WordListView,
    WordDetailView,
)

urlpatterns = [
    path('', WordListView.as_view(), name='vocab'),
    path('<int:pk>/', WordDetailView.as_view(), name='word'),
]