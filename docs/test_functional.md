Functional Tests
================

Functional tests examine if the app works from the user's perspective. This is typically the first test written for a 
project as it identifies the key requirements for your website to be usable.   
While unit tests check the code logic is correct, functional tests check that the app's flow is correct.  
The functional test cases can be based on user stories, which is the flow a user would take while interacting with your 
 website.  

Below is a simple workflow a user may take to search for a product on your website:  
1. Open a browser and navigate to your search page
2. Enter in a string in the search form, then submit the form
3. See the search results

Translating that story into actual Python code is not too different:
```python
class SearchProductTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)
    
    def tearDown(self):
        self.browser.quit()

    def test_search(self):
        # 1. Bob navigates to search page
        self.browser.get(self.live_server_url + reverse('product:search'))
        
        # 2. Bob enters in a string in the search form and submits it
        input = self.browser.find_element_by_id('search-input')
        input.send_keys('asus\n')
        
        # 3. See the search results
        table = self.browser_find_element_by_id('search-table')
        rows = table.find_element_by_tag_name('tr')
        self.assertIn('asus', [row.text for row in rows])  
```

To run this test:
```commandline
python3 manage.py test functional_tests.test_search_product.SearchProductTest
```

I am using Selenium to open a Firefox browser, submitting a search string, then checking the results. As this actually
opens up the browser to perform the actions, the interactions can simulate how a user can interact with your site's UI
elements.  

Additionally, the browser may take some time to load resources. I have asked the browser to `implicitly_wait`, which is 
to give the browser time to load before throwing an exception. Other options include
[explicit wait and fluent wait](http://toolsqa.com/selenium-webdriver/implicit-explicit-n-fluent-wait/).


### Functional tests drive Unit tests
After we run and fail this test, we are ready to break down the steps needed to pass the test.  
For example:
```python
# 1. Bob navigates to search page
self.browser.get(self.live_server_url + reverse('product:search'))
```
__View tests__
- Does the url go to the right view?  

```python
# 2. Bob enters in a string in the search form...
input = self.browser.find_element_by_id('search-input')
```
__View tests__
- Does the view return the right template?
- Does the template have an input field?  

```python
# 2. ...Bob submits the form
input.send_keys('asus\n')
```
__View tests__
- Which view handles the search query?  
__Form tests__
- Does the form handle input validation?  
__Model tests__
- How are Products saved in the app?  
- Does the Product have the right fields to search by?
 
 ```python
# 3. See the search results
table = self.browser_find_element_by_id('search-table')
rows = table.find_element_by_tag_name('tr')
self.assertIn('asus', [row.text for row in rows])
```
__View tests__
- How does the app search for Products?
- Does the view return the right template?
- Does the template have a table for search results?
- Is it passing the correct data back to the template?
