from django.urls import reverse

from functional_tests.FunctionalTest import FunctionalTest


class SearchProductTest(FunctionalTest):
    def test_search_products(self):
        # User visits website
        self.browser.get(self.live_server_url + reverse('product:search'))

        # User accidentally submits an empty query
        # They hit Enter on the empty input box
        self.get_item_input_box().send_keys('\n')

        # The page refreshes and there is an error message saying search cannot be blank
        error = self.get_error_element()
        self.assertEqual(error.text, 'Please enter text to search by')

        # User tries again with some random text this time, which now works
        # The page refreshes and tells them the there are no products matching that name
        self.get_item_input_box().send_keys('abcd1234\n')
        error = self.get_error_element()
        self.assertEqual(error.text, 'No results. Please try again')

        # User tries again with a known products name
        # The page refreshes and the user can see a list of items matching that name
        self.get_item_input_box().send_keys('epson')
        self.check_for_row_in_list_table('epson', 'product-table')

        # User searches again for a different product
        # The page refreshes and the user can see a different list of items
        self.get_item_input_box().send_keys('asus')
        self.check_for_row_in_list_table('asus', 'product-table')
