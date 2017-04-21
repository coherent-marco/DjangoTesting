from django.utils.translation import ugettext as _
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

from utils.models import MultilingualModel, MultilingualTranslation, RangeLinearizationMetaClass

from collections import namedtuple

PAYMENT_MODE_CHOICES = (
    (0, _('single premium')),
    (1, _('monthly')),
    (2, _('quarterly')),
    (3, _('semiannual')),
    (4, _('annual')),
)

Insured = namedtuple('Insured', ['age', 'gender', 'smoking'])

class Currency(models.Model):
    code = models.CharField(max_length=3, validators=[MinLengthValidator(3)], primary_key=True)

class ExchangeRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    effective_date = models.DateField()

    class Meta:
        unique_together = ('currency', 'effective_date')

class Insurer(MultilingualModel):
    code = models.CharField(max_length=20, primary_key=True)
    contact_no = models.CharField(max_length=20, null=True, blank=True)
    fax_no = models.CharField(max_length=20, null=True, blank=True)
    default_currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL)
    last_update = models.DateTimeField(auto_now=True)

class InsurerTranslation(MultilingualTranslation):
    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE)
    insurer_name = models.CharField(max_length=100)
    insurer_official_name = models.CharField(max_length=100)
    official_website = models.URLField()
    description = models.TextField(null=True, blank=True)
    office_address = models.TextField(null=True, blank=True)
    offerings = models.TextField(null=True, blank=True)
    special_features = models.TextField(null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta(MultilingualTranslation.Meta):
        unique_together = ('insurer', 'language')

class InsurerRating(MultilingualModel):
    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE, related_name='ratings')
    rating_agency = models.CharField(max_length=100)
    rating = models.CharField(max_length=10)
    effective_date = models.DateField()

    class Meta:
        unique_together = ('insurer', 'rating_agency', 'effective_date')

class Product(MultilingualModel):
    id = models.CharField(max_length=50, primary_key=True)
    insurer = models.ForeignKey(Insurer, null=True, on_delete=models.SET_NULL)
    currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL)
    issue_age_from = models.SmallIntegerField(null=True, blank=True)
    issue_age_to = models.SmallIntegerField(null=True, blank=True)
    effective_date = models.DateField()
    active = models.BooleanField()
    last_update = models.DateTimeField(auto_now=True)

    @classmethod
    def get_queryset(cls, prefetches=None, **kwargs):
        queryset = cls.objects.all()

        if prefetches is None:
            prefetches = []
        elif prefetches == '*':
            prefetches = cls.prefetches
        elif isinstance(prefetches, str):
            prefetches = [prefetches]

        for lookup in prefetches:
            queryset = cls.get_prefetched(queryset, lookup, **kwargs)

        return queryset

    class Meta(MultilingualModel.Meta):
        abstract = True

    def clean(self):
        super().clean()
        if self.issue_age_from is not None and self.issue_age_to is not None:
            if self.issue_age_from > self.issue_age_to:
                raise ValidationError('Invalid issue age limits: [%d, %d]' %(self.issue_age_from, self.issue_age_to))


class ProductTranslation(MultilingualTranslation):
    product_name = models.CharField(max_length=500)
    brochure_link = models.URLField(blank=True, null=True)
    # TODO: Replace the two below by FileField and ImageField respectively
    brochure = models.CharField(max_length=500, blank=True, null=True)
    brochure_image = models.CharField(max_length=500, blank=True, null=True)

    tag1 = models.TextField(null=True, blank=True)
    tag2 = models.TextField(null=True, blank=True)
    risks = models.TextField(null=True, blank=True)

    class Meta(MultilingualTranslation.Meta):
        abstract = True

class Premium(models.Model):
    age = models.SmallIntegerField()
    gender = models.BooleanField()
    smoking = models.BooleanField()
    payment_mode = models.SmallIntegerField(choices=PAYMENT_MODE_CHOICES)

    class Meta(MultilingualTranslation.Meta):
        abstract = True
