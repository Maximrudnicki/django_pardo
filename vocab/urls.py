from django.urls import path
from .views import WordList, WordDetail, WordCreate, WordUpdate, WordDelete

urlpatterns = [
    path('', WordList.as_view(), name='vocab'),
    path('<int:pk>/', WordDetail.as_view(), name='word'),
    path('word-create/', WordCreate.as_view(), name='word-create'),
    path('word-update/<int:pk>/', WordUpdate.as_view(), name='word-update'),
    path('word-delete/<int:pk>/', WordDelete.as_view(), name='word-delete'),
]