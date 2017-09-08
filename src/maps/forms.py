from django import forms


class PostAddForm(forms.Form):
    title = forms.CharField()
    contents = forms.CharField()
    location = forms.CharField(required=False)

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title == "":
            raise forms.ValidationError("Not a valid title")
        return title
