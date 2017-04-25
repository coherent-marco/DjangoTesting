from django.test import TestCase
from django.core.exceptions import ValidationError

from products.models import TermProduct, TermPremium
from products.helpers import Insured

class TermProductTest(TestCase):
    def setUp(self):
        self.term_product_entry = {
            'issue_age_from': 18,
            'issue_age_to': 65,
            'sum_assured_min': 100000,
            'sum_assured_max': 99999999,
            'is_mortgage_term': False,
            'premium_term_type': 'to_age',
            'premium_term_parameter': 85,
            'level_premium': True,
            'coverage_term_type': 'fixed_term',
            'coverage_term': 10,
            'death_benefit_percentage': 1.0,
            'sum_assured_pattern': 'level',
        }

        self.term_premium_entries = [
            {
                'age': 18,
                'gender': True,
                'smoking_status': False,
                'payment_mode': 'monthly',
                'sum_assured_band_from': None,
                'sum_assured_band_to': 1000000,
                'intercept': 0,
                'slope': 0.015,
            },
            {
                'age': 18,
                'gender': True,
                'smoking_status': False,
                'payment_mode': 'monthly',
                'sum_assured_band_from': 1000001,
                'sum_assured_band_to': None,
                'intercept': 0,
                'slope': 0.014,
            }
        ]

    def test_save_and_retrieve(self):
        term_product = TermProduct(**self.term_product_entry)
        term_product.save()

        term_premiums = [
            TermPremium(**entry) for entry in self.term_premium_entries
        ]
        term_product.add(*term_premiums)
        term_product.save()

        term_products = TermProduct.objects.all()
        first_term_product = term_products[0]
        first_term_product_premiums = first_term_product.termpremium_set.all()

        self.assertEqual(len(term_products), 1, 'Found %s products' % len(term_products))
        self.assertEqual(len(first_term_product_premiums), 2, 'Found %s premium record(s) in the first term product' % len(first_term_product_premiums))

        self.assertEqual(first_term_product.issue_age_from, 18)
        self.assertEqual(first_term_product.issue_age_to, 65)
        self.assertEqual(first_term_product.sum_assured_min, 100000)
        self.assertEqual(first_term_product.sum_assured_max, 99999999)
        self.assertEqual(first_term_product.is_mortgage_term, False)
        self.assertEqual(first_term_product.premium_term_type, 'to_age')
        self.assertEqual(first_term_product.premium_term_parameter, 85)
        self.assertEqual(first_term_product.level_premium, True)
        self.assertEqual(first_term_product.coverage_term_type, 'fixed_term')
        self.assertEqual(first_term_product.coverage_term, 10)
        self.assertAlmostEqual(first_term_product.death_benefit_percentage, 1.0)
        self.assertEqual(first_term_product.sum_assured_pattern, 'level')

    def test_premium_term(self):
        term_product = TermProduct.objects.create(**self.term_product_entry)
        term_product.premium_term_type = 'to_age'
        term_product.premium_term_parameter = 85
        term_product.insured = Insured(age=30, gender=True, smoking_status=False)

        self.assertEqual(term_product.premium_term, 55, 'Premium term is %s' % term_product.premium_term)

    def test_issue_age_from_less_than_issue_age_to(self):
        term_product = TermProduct.objects.create(**self.term_product_entry)
        term_product.issue_age_from = 50
        term_product.issue_age_to = 20

        with self.assertRaises(ValidationError):
            term_product.save()

    def test_min_sa_less_than_max_sa(self):
        term_product = TermProduct.objects.create(**self.term_product_entry)
        term_product.sum_assured_min = 100000
        term_product.sum_assured_max = 10000

        with self.assertRaises(ValidationError):
            term_product.save()

    def test_active_default_true(self):
        term_product = TermProduct.objects.create(**self.term_product_entry)

        self.assertEqual(term_product.active, True, 'default active is %s' % term_product.active)