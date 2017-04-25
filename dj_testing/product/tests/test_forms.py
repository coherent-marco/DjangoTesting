from django.test import TestCase

from product.forms import SearchForm


class SearchFormTest(TestCase):
    def test_form_renders_input_with_placeholders_and_css_classes(self):
        form = SearchForm()

        self.assertIn('placeholder="Enter your search term"', form.as_p())
        self.assertIn('class="form-control', form.as_p())
        self.assertIn('id="input-search', form.as_p())

    def test_form_validation_blank_search(self):
        form = SearchForm(data={})

        self.assertFalse(form.is_valid())
        self.assertIn('query', form.errors)