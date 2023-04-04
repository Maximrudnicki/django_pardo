from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Permission

from ..models import Word
from ..mixins import WordAccessMixin
from ..views import WordDelete


class WordListTest(TestCase):
    def test_word_list_view(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        url = reverse('vocab')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vocab/vocab.html')

    def test_word_list_view_with_words(self):
        user = User.objects.create_user(username='testuser', password='12345')
        word1 = Word.objects.create(
            word='apple', definition='a fruit', user=user)
        word2 = Word.objects.create(
            word='orange', definition='a fruit', user=user)
        self.client.login(username='testuser', password='12345')
        url = reverse('vocab')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vocab/vocab.html')
        self.assertContains(response, word1.word)
        self.assertContains(response, word2.word)


class WordDetailTest(TestCase):
    def test_word_detail_view(self):
        user = User.objects.create_user(username='testuser', password='12345')
        word = Word.objects.create(
            word='apple', definition='a fruit', user=user)
        self.client.login(username='testuser', password='12345')
        url = reverse('word', kwargs={'pk': word.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vocab/word_detail.html')
        self.assertContains(response, word.word)
        self.assertContains(response, word.definition)


class WordCreateTest(TestCase):
    def test_word_create_view(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        url = reverse('word-create')
        data = {
            'word': 'apple',
            'definition': 'a fruit',
            'learned': False,
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vocab'))
        self.assertEqual(Word.objects.count(), 1)
        word = Word.objects.first()
        self.assertEqual(word.word, 'apple')
        self.assertEqual(word.definition, 'a fruit')
        self.assertEqual(word.learned, False)
        self.assertEqual(word.user, user)


class WordUpdateTest(TestCase):
    def test_word_update_view(self):
        user = User.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpass'
        )
        word = Word.objects.create(word='apple', definition='a fruit', user=user)
        url = reverse('word-update', kwargs={'pk': word.pk})
        self.client.login(username='testuser', password='testpass')

        response = self.client.post(url, {
            'word': 'updated_word',
            'definition': 'updated_definition',
            'learned': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('vocab'))

        word.refresh_from_db()
        self.assertEqual(word.word, 'updated_word')
        self.assertEqual(word.definition, 'updated_definition')
        self.assertTrue(word.learned)


class WordDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.word = Word.objects.create(
            word='testword',
            definition='testdefinition',
            user=self.user
        )
        self.client = Client()
        self.url = reverse('word-delete', kwargs={'pk': self.word.pk})
        self.client.login(username='testuser', password='testpass')

    def test_word_delete_view_access_forbidden(self):
        """Test that access is forbidden if user does not own word"""
        other_user = get_user_model().objects.create_user(
            username='otheruser',
            password='otherpass'
        )
        self.client.force_login(other_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_word_delete_view_access_allowed(self):
        """Test that access is allowed if user owns word"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Word.objects.filter(pk=self.word.pk).exists())

    def test_word_delete_view_login_required(self):
        """Test that login is required to access view"""
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            f'/accounts/login/?next={self.url}'
        )

    def test_word_delete_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        self.client.logout()
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'vocab/word_confirm_delete.html')

    def test_word_delete_view_has_correct_mixin(self):
        """Test that the view uses the correct mixin"""
        self.assertTrue(issubclass(WordDelete, WordAccessMixin))

    def test_word_delete_view_has_permission(self):
        """Test that user has the required permission to access view"""
        permission = Permission.objects.get(codename='delete_word')
        self.user.user_permissions.add(permission)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Word.objects.filter(pk=self.word.pk).exists())
