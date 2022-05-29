from django import forms


class PostSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search ..."}),
                             label="")
