Form Testing
============
 
Forms in Django serve multiple purposes - it can be used to:
+ render an actual HTML form
+ validate the user input, 
+ show validation errors to the user
+ create/update model if using `ModelForm`

Therefore your tests will need to cover all of these features you want to use.
  
If your models are __only__ created via a form, you can transfer a lot of the model validation logic to it.  

A basic sample test showing a `forms.Form` validation:
```python
from django.test import TestCase

from app.products.forms import SearchForm, EMPTY_SEARCH_ERROR


class SearchFormTest(TestCase):
    def test_form_renders_search_text_input(self):
        form = SearchForm()

        self.assertIn('placeholder="Enter a search terrm"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
        
        
    
    def test_form_validation_for_blank_input(self):
        form = SearchForm(data={'text': ''})
        
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'], [EMPTY_SEARCH_eRROR]
        )
```

An basic sample test showing a `ModelForm` validation:
```python
from django.test import TestCase

from app.models import Blog, ERROR_EMPTY_TITLE, ERROR_EMPTY_CONTENT
from app.forms import BlogForm


class BlogFormTest(self):
    def test_form_save(self):
        form = BlogForm(data={
            'title': 'this is the title',
            'content': 'this is the blog content'
        })
        self.assertTrue(form.is_valid())
        new_blog = form.save()
        
        self.assertEqual(new_blog.title, 'this is the title')
        self.assertEqual(new_blog.content, 'this is the blog content')

    def test_form_empty_title_error(self):
        form = BlogForm(data={
            'title': '',
            'content': 'this is the blog content'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(forms.errors['title'], [ERROR_EMPTY_TITLE])
    
    def test_form_empty_desc_error(self):
         form = BlogForm(data={
            'title': 'this is the title',
            'content': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(forms.errors['content'], [ERROR_EMPTY_CONTENT])

```