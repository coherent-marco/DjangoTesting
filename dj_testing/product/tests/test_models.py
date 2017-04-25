from django.test import TestCase

from product.models import Product


class ProductTest(TestCase):
    def test_save_and_retrieve(self):
        product = Product()
        product.code = 'c0001'
        product.save()

        ps = Product.objects.all()
        p1 = ps[0]

        self.assertEqual(p1.code, 'c0001')

    def test_string_representation(self):
        p = Product.objects.create(
            code='c0001'
        )

        self.assertEqual(str(p), 'Product %s' % (p.pk, ))

    def test_optional_fields(self):
        p = Product.objects.create(
            code='c0001',
            contact_no = '+852 1234 5678',
            fax_no = '+852 9876 5432',
        )

        ps = Product.objects.all()
        p1 = ps[0]

        self.assertEqual(p1.code, 'c0001')
        self.assertEqual(p1.contact_no, '+852 1234 5678')
        self.assertEqual(p1.fax_no, '+852 9876 5432')