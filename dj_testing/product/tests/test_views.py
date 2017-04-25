from django.test import TestCase, RequestFactory
# Create your tests here.
from django.urls import reverse

from product.forms import SearchForm


class ProductSearchTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def tearDown(self):
        pass

    def test_search_page_resolves_to_view(self):
        response = self.client.get(reverse('product:search'))
        self.assertEqual(response.status_code, 200)

    def test_search_page_renders_search_template(self):
        response = self.client.get(reverse('product:search'))
        self.assertTemplateUsed(response, 'product/index.html')

    # Do unit tests for forms (SearchForm)
    def test_search_page_renders_search_form(self):
        response = self.client.get(reverse('product:search'))
        self.assertIsInstance(response.context['form'], SearchForm)

    # Continue with view tests when form test is complete
    # Do unit tests for models (Product)
    def test_retrieves_product_from_filter(self):
        response = self.client.get(reverse('product:search'), data={
            'query': 'lenovo'
        })
        self.assertIsInstance(response.context['form'], SearchForm)

