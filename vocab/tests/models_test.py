from django.test import TestCase
from django.contrib.auth import get_user_model

from datetime import datetime

from ..models import Word


class WordModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser', password='testpass')
        cls.word = Word.objects.create(
            user=cls.user,
            word='testword',
            definition='testdefinition',
            learned=False,
            added=datetime.now()
        )

    def test_word_str(self):
        self.assertEqual(str(self.word), 'testword - testdefinition')

    def test_word_by_user(self):
        qs = Word.objects.by_user(self.user)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.word)
