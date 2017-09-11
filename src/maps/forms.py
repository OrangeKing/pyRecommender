from django import forms

from .models import Post


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'contents',
            'location'
        ]
    
        def clean_title(self):
            title = self.cleaned_data.get("title")
            if title == "":
                raise forms.ValidationError("Not a valid title")
            return title
