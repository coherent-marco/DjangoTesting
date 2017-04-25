View Testing
============

Django Views decide _what_ data is presented to the user.  
_How_ the data looks is __not__ part of the view's concerns.   

Essentially, a URL maps to a Python function that describes which data is presented.
As a __minimum__, you should test the URL renders your expected template/resolves to your expected view.  

A sample view test may be like this:  
_Core tests_
+ Test if the URL resolves to the view
+ Test if the view renders the correct template/HTML

_Logic tests_  
+ Test if the view passes the correct data to the template to render
+ Test how error messages are shown
+ If handling user input:
    + Test if the user can/cannot create, update or delete an object
    + Test that your view uses the form for input validation
    _Note_: input validation isn't handled by the view directly


An example basic test:
```python
from django.test import TestCase

from app.models import Product


class SearchViewTest(TestCase):
    def test_search_page_resolves_to_view(self):
        response = self.client.get(reverse('product:search'))
        self.assertEqual(response.status_code, 200)

    def test_search_page_renders_search_template(self):
        response = self.client.get(reverse('product:search'))
        self.assertTemplateUsed(response, 'search.html')
    
    def test_search_page_uses_search_form(self):
        response = self.client.get(reverse('product:search'))
        self.assertIsInstance(response.context['form'], SearchForm)
```

You may improve readability by splitting the tests for a view into multiple classes based on
 its functions  
 
```python
class SearchViewIntegratedTest(TestCase):
    def test_search_retrieves_correct_data(self):
        p1 = Product.objects.create(name='lenovo')
        p2 = Product.objects.create(name='ibm')
        
        response = self.client.get(reverse('product:search'), data={'query': 'lenovo'})
    
        self.assertContains(p1, response.context['results'])
        self.assertNotIn(p2, response.context['results'])
    
    def test_search_error_message(self):
        response = self.client.get(reverse('product:search'), data={'query': ''})
        self.assertContains(response, EMPTY_SEARCH_ERROR)
        
    def test_invalid_input_renders_search_page(self):    
        response = self.client.get(reverse('product:search'), data={'query': ''})
        self.assertTemplateUsed(response, 'search.html')
```