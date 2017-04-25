from django.db import models

# Create your models here.
class Product(models.Model):
    code = models.CharField(max_length=20)
    contact_no = models.CharField(max_length=20, blank=True)
    fax_no = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return 'Product %s' % (self.pk, )


class ParticipatingDetailValues(models.Model):
    # Filters
    ProdID = models.CharField(max_length=50)
    Age = models.IntegerField()
    Gender = models.BooleanField()
    Smoker = models.BooleanField()
    PolicyYear = models.IntegerField()
    SumAssuredFrom = models.IntegerField()
    SumAssuredTo = models.IntegerField()
    # Constants for generating values
    # Guranteed
    GuarCashValue_intercept = models.IntegerField()
    GuarCashValue_slope = models.FloatField()
    GuarDeathBenefit_intercept = models.IntegerField()
    GuarDeathBenefit_slope = models.FloatField()
    # Non Guar
    NonGuarCashValue_intercept = models.IntegerField()
    NonGuarCashValue_slope = models.FloatField()
    NonGuarTCashValue_intercept = models.IntegerField()
    NonGuarTCashValue_slope = models.FloatField()
    NonGuarDeathBenefit_intercept = models.IntegerField()
    NonGuarDeathBenefit_slope = models.FloatField()
    NonGuarTDeathBenefit_intercept = models.IntegerField()
    NonGuarTDeathBenefit_slope = models.FloatField()

    # Entry Meta Data
    LastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = [
            ['Age', 'Gender','Smoker','ProdID'],
        ]