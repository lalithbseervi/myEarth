from django import forms

from .models import Post
from crispy_forms.layout import Row, Column, Submit, Layout
from crispy_forms.helper import FormHelper

# from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    content = forms.Textarea(attrs={'placeholder': 'Describe your query.'})

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
        ]
     
    widgets = {
        'title': forms.TextInput(attrs={'placeholder': 'Enter a title'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_layout(
            Layout(
                Row(
                    Column('title'), css_class='self-start'
                ),
                Row(
                    Column('content'), css_class='self-start', template='rte.html' 
                ),
                Row(
                    Submit('submit', 'Ask Question'), css_class='self-start border border-gray-950 rounded rounded-md flex justify-center p-2 bg-green-500 arc-btn-retro mt-2 md:mt-4'
                )
            )
        )

class EditPost(forms.ModelForm):
    content = forms.Textarea()

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_layout(
            Layout(
                Row(
                    Column('title'), css_class='self-start'
                ),
                Row(
                    Column('content'), css_class='self-start'
                ),
                Row(
                    Submit('submit', 'Edit Question'), css_class='self-start border border-gray-950 rounded rounded-md flex justify-center p-2 bg-green-500 arc-btn-retro mt-2 md:mt-4'
                )
            )
        )