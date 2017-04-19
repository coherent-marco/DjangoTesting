Testing Guidelines
==================

There are generally three phases in a test:   
1. Setup - Create the test conditions
2. Testing - Run the code you want to test 
3. Verification - Check if the code performed as expected
4. Clean up - Remove any artifacts created by the test

###Test Driven Development
1. Add a new test
2. Run all tests and check the new test fails for the expected reason.  
Gives confidence in the new test 
3. Write the minimal amount of code needed to pass the test (and nothing more).  
Allowed to be 'hacky'
4. Run all tests to see if it passes and does not break existing features
5. Refactor code and re-run tests
+ Hacky solutions are fixed here
+ Duplicate code should be extracted (after ~3 duplicates)
+ Magic numbers should be removed
+ Growing methods/objects can be broken up

Running the test after each edit gives confidence that the change does not alter existing functions. 

### Best Practices
+ Each test does one thing  
+ Tests should be quick to run
+ Do not test third party code
+ Do not have test cases depend on each other
+ Do not have test cases depend on system state caused by another test

### Django specific notes
Django automatically creates a `test.py` for each app - this is insufficient for any thorough testing.  
Instead, create a `test` Python package. In that folder, create your test files: `test_models.py`, `test_views.py` (as 
well as `test_forms.py` or `test_serializers` if you have them).

Django's TestCase is class based - typically each test class examines one Python class.  
Within each test class, Django will autodiscover the test methods which begin with `test_*`.  

In each test file, the structure is generally as follows:
```python
from django.test import TestCase
from myapp.helpers import Calculator

class SomeModelTest(TestCase):
    def setUp(self):
        # Code Django will run before each test
        # Set up your test environment here
        # eg. Create a fake user account if needed
        pass
    
    def tearDown(self):
        # Code Django will run after each test
        # Clear the system of any test artefacts here
        # eg. Delete any files generated by the test
        pass

    # General test format
    def test_calculator_add(self):
        # 1. Set up the test
        calc = Calculator()
        
        # 2. Perform the logic
        result = calc.add(1, 2)
        
        # 3. Check if the test passed or failed
        self.assertEquals(result, 3)
        # Generally the format is (value1, value2, error message)
        # Other assertions:
        # self.assertTrue(value1, value2)
        # self.assertFalse(value1, value2)
        # self.assertIn(needle, haystack)        
        # Refer to https://docs.djangoproject.com/en/dev/topics/testing/tools/#assertions for a complete list
        
    # Alternative test format for checking exceptions
    def test_divide_by_zero(self):
        # 1. Set up the test
        calc = Calculator()
        
        # 3. Check error was raised
        with self.assertRaises(ValueError):
            # 2. Perform the logic
            calc.divide(12, 0)    
    
```