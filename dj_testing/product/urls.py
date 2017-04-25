from django.conf.urls import url

from product.views import SearchView

urlpatterns = [
    (url(r'^search', SearchView.as_view(), name='search')),
]