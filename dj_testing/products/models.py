from django.db import models


class TermProduct(models.Model):
    pass


class TermPremium(models.Model):
    product = models.ForeignKey(
        'TermProduct',
        on_delete=models.CASCADE,
    )
