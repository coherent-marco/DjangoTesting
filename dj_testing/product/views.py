from django.shortcuts import render

# Create your views here.
from django.views import View

from product.forms import SearchForm


class SearchView(View):
    def get(self, request):
        form = SearchForm()
        return render(request, 'product/index.html', {'form': form})