from django.test import TestCase
import time
from .models import Word


class TestWordModel(TestCase):
    def setUp(self):
        Word.objects.create(word='thursday', definition='четверг')
        time.sleep(0.5)
        Word.objects.create(word='wensday', definition='среда')
        time.sleep(0.5)
        Word.objects.create(word='sunday', definition='воскресенье')

    def test_learned_default_should_be_false(self):
        word = Word.objects.get(word='thursday')
        self.assertEqual(word.learned, False)

    def test_words_order(self):
        objects = Word.objects.all().order_by('-added')
        self.assertEqual(objects[0].word, 'sunday')
        self.assertEqual(objects[1].word, 'wensday')
        self.assertEqual(objects[2].word, 'thursday')