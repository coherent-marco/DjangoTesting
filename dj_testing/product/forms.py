from django import forms



class SearchForm(forms.Form):
    query = forms.CharField(label='Search Input', max_length=50,
                            widget=forms.TextInput(attrs={
                                'placeholder': 'Enter your search term',
                                'class': 'form-control',
                                'id': 'input-search',
                            }))
