from django import forms


class PostCreateForm(forms.Form):
    title = forms.CharField()
    contents = forms.Textarea()
    location = forms.CharField(required=False)
