from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Word
from .serializers import WordSerializer


class WordListView(generics.ListCreateAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Word.objects.by_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Word.objects.by_user(self.request.user)
