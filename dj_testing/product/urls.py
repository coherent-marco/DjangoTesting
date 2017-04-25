from django.conf.urls import url

urlpatterns = [
    (url(r'^search', SearchView.as_view(), name='search')),
]