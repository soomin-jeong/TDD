from django.test import TestCase
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from .views import HomePageView

from django.http import HttpRequest

from .models import Item


# Create your tests here.

class SmokeTest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(2**3, 8, msg='the equation fails')


class HomePageTest(TestCase):
    # def test_the_root_url_finds_the_home_page_view(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, HomePageView, msg='Cannot find a view for homepage')

    def test_homepage_returns_correct_html(self):

        # HttpRequest object is what Django gets when a user asks for a page
        request = HttpRequest()
        response = HomePageView(request)

        expected_html = render_to_string('home.html')

        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>To-do list</title>', response.content)
        # self.assertTrue(response.content.endswith(b'</html>'))
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        HomePageView(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_can_save_a_POST_request(self):

        # HttpRequest object is what Django gets when a user asks for a page
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = HomePageView(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )
        self.assertEqual(response.content.decode(), expected_html)


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first(ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item, 'The first(ever) list item')
        self.assertEqual(second_saved_item,  'The second list item')
