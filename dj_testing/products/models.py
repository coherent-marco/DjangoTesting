from django.db import models

TERM_TYPE_CHOICES = (
    ('fixed_term', 'fixed term'),
    ('to_age', 'to age'),
)

SUM_ASSURED_PATTERN_CHOICES = (
    ('level', 'level sum assured'),
    ('increasing', 'increasing sum assured'),
    ('decreasing', 'decreasing sum assured'),
)

PAYMENT_MODE_CHOICES = (
    ('single_premium', 'single premium'),
    ('monthly', 'monthly'),
    ('quarterly', 'quarterly'),
    ('semiannual', 'semi-annual'),
    ('annual', 'annual'),
)


class TermProduct(models.Model):
    issue_age_from = models.PositiveSmallIntegerField(null=True, blank=True)
    issue_age_to = models.PositiveSmallIntegerField(null=True, blank=True)
    sum_assured_min = models.PositiveIntegerField(default=0)
    sum_assured_max = models.PositiveIntegerField(default=2147483647)   # Max value of PositiveIntegerField
    is_mortgage_term = models.BooleanField()
    premium_term_type = models.CharField(choices=TERM_TYPE_CHOICES, max_length=30)
    premium_term_parameter = models.SmallIntegerField()
    level_premium = models.BooleanField()
    coverage_term_type = models.CharField(choices=TERM_TYPE_CHOICES, max_length=30)
    coverage_term_parameter = models.SmallIntegerField()
    death_benefit_percentage = models.FloatField()
    sum_assured_pattern = models.CharField(choices=SUM_ASSURED_PATTERN_CHOICES, max_length=30)


class TermPremium(models.Model):
    product = models.ForeignKey(
        'TermProduct',
        on_delete=models.CASCADE,
    )
    age = models.PositiveSmallIntegerField()
    gender = models.BooleanField()
    smoking_status = models.BooleanField()
    payment_mode = models.CharField(choices=PAYMENT_MODE_CHOICES, max_length=30)
    sum_assured_band_from = models.PositiveIntegerField(null=True, blank=True)
    sum_assured_band_to = models.PositiveIntegerField(null=True, blank=True)
    intercept = models.FloatField()
    slope = models.FloatField()