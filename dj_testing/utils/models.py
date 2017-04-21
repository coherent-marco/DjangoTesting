from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import get_language

import pandas as pd

class MultilingualModelMetaClass(type(models.Model)):
    @property
    def translations_objects(self):
        return self.translations.rel.related_model.objects
    @property
    def reverse_query_name(self):
        return self.translations.rel.remote_field.name
    @property
    def reverse_query_id(self):
        return '%s_id' %self.translations.rel.remote_field.name

class MultilingualModel(models.Model, metaclass=MultilingualModelMetaClass):
    translation_fields = None
    _translation = None

    class Meta:
        abstract = True

    @property
    def current_language(self):
        if self._translation is not None:
            return self._translation.language

    def get_translation_fields(self):
        if self.translation_fields is None and hasattr(type(self), 'translations'):
            self.translation_fields = []
            for field in type(self).translations.rel.related_model._meta.fields:
                if not isinstance(field, (models.AutoField, models.fields.related.RelatedField)):
                    self.translation_fields.append(field.column)

        return self.translation_fields or []

    def get_translation(self, lang=settings.LANGUAGE_CODE):
        if self.translations.count() == 1:
            _translation = self.translations.all()[0]
        else:
            try:
                _translation = self.translations.get(language=lang)
            except ObjectDoesNotExist:
                _translation_unique_key = {
                    type(self).reverse_query_id: self.pk,
                    'language': settings.LANGUAGE_CODE,
                }
                _translation = type(self).translations_objects.get(**_translation_unique_key)

        return _translation

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __getattr__(self, name):
        if self.translation_fields is None or name == 'translation_fields':
            self.translation_fields = self.get_translation_fields()

        if name in self.translation_fields:
            lang = get_language()

            if self._translation is None or self.current_language != lang:
                try:
                    self._translation = self.get_translation(lang)
                except ObjectDoesNotExist:
                    raise AttributeError

            return getattr(self._translation, name)
        else:
            return models.Model.__getattribute__(self, name)

class MultilingualTranslation(models.Model):
    language = models.CharField(max_length=20)

    class Meta:
        abstract = True
        default_related_name = 'translations'

    def clean(self):
        self.language = self.language.lower()
        if self.language not in [lang[0].lower() for lang in settings.LANGUAGES]:
            raise ValidationError({
                'language': 'Invalid language code: %s' %self.language,
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class RangeLinearizationMetaClass(type(models.Model)):
    def __new__(metacls, name, bases, namespace, **kwargs):
      return super().__new__(metacls, name, bases, namespace)

    def __init__(cls, name, bases, namespace, column, suffix_from='from', suffix_to='to', **kwargs):
        cls.column = column
        cls.suffix_from, cls.suffix_to = suffix_from, suffix_to

        if kwargs.get('drop_labels') is not None:
            cls.drop_labels = kwargs.get('drop_labels')
        else:
            cls.drop_regex = kwargs.get('drop_regex', r'^(?!.*id$)')

        super().__init__(name, bases, namespace)

    def get_groupby(cls):
        if not hasattr(cls, 'groupby') or cls.groupby is None:
            groupby = None
        elif isinstance(cls.groupby, list):
            groupby = cls.groupby
        elif isinstance(cls.groupby, str):
            groupby = [cls.groupby]

        return groupby

    def get_linearized_values(cls, queryset):
        column = cls.column
        column_from = '%s_%s' %(cls.column, cls.suffix_from)
        column_to = '%s_%s' %(cls.column, cls.suffix_to)
        groupby = cls.get_groupby()

        if isinstance(queryset, models.QuerySet):
            values_list = list(queryset.values())
        else:
            values_list = list(queryset)

        df = pd.DataFrame.from_dict(values_list)
        df_trans = pd.DataFrame()

        if hasattr(cls, 'drop_labels'):
            df = df.drop(cls.drop_labels, axis=1)
        elif hasattr(cls, 'drop_regex'):
            df = df.filter(regex=cls.drop_regex, axis=1)

        if groupby is None:
            df_trans = cls.get_linearized_subset(df, column, column_from, column_to)
        else:
            for group, subset in df.groupby(groupby):
                subset_trans = cls.get_linearized_subset(subset, column, column_from, column_to)
                df_trans = df_trans.append(subset_trans)

        return df_trans
#
    @staticmethod
    def get_linearized_subset(subset, column, column_from, column_to):
        subset_trans = pd.DataFrame()
        for ix, row in subset.iterrows():
            range_from = row[column_from] or 0
            range_to = row[column_to] or 100
            if range_from == range_to:
                row_trans = row
                row_trans[column] = range_from
                row_trans = row_trans.drop([column_from, column_to])
            else:
                row_trans = pd.DataFrame(list(range(int(range_from), int(range_to) + 1)), columns=[column])
                for key, value in row.drop([column_from, column_to]).iteritems():
                    row_trans[key] = value
            subset_trans = subset_trans.append(row_trans)
        return subset_trans



from django.db import connection

class Utils():
    def __init__(self):
        pass

    def ResultToList(self, resultData):
        return list(resultData)

def ExecStoredProc(storedprocname, paramsdict='', database='Seasonalife'):
    # raise error if nothing provided
    if storedprocname is None:
        raise ValueError('AzureSQL - ExecStoredProc error occurred.')
    # Initilazation
    # try:
    # conn = pyodbc.connect('Driver={SQL Server};Server=tcp:coherentdev.database.windows.net,1433; +
    # Database=' + database + ';Uid=dbadmin@coherentdev;Pwd=SqlDev#2016;')
    # 	conn.autocommit = True
    # 	#Sample : "exec sp_TestGetSummaryByCountry @ASSETCATEGORY = 'CASH', @COUNTRY = 'AIA' "
    # 	sql = "exec " + storedprocname + " " + paramsdict
    # 	resultData = pd.read_sql_query(sql, conn)
    # except Exception as e:
    # 	raise e
    # finally:
    # 	conn.close()

    sql = "exec " + storedprocname + " " + paramsdict
    resultData = pd.read_sql_query(sql, connection)
    return resultData
