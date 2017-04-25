from django.shortcuts import render

# Create your views here.
from django.views import View


class SearchView(View):
    def get(self):
        return