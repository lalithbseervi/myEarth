from django import forms
from django.contrib.auth import (authenticate, get_user_model)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username = username, password = password)
            if user is None:
                raise forms.ValidationError("Incorrect username or password.")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_layout(
            Layout(
                Row(
                    Column('username'), css_class='self-start w-full'
                ),
                Row(
                    Column('password'), css_class='self-start w-full'
                ),
                Row(
                    Submit('submit', 'Login'), css_class='self-start w-full border border-gray-950 rounded rounded-md flex justify-center p-2 bg-green-500 arc-btn-retro'
                )
            )
        )

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'johndoe'}))
    email = forms.EmailField(label='Email Address', widget=forms.TextInput(attrs={'placeholder': 'johndoe@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_layout(
            Layout(
                Row(
                    Column('username'), css_class='self-start w-full',
                ),
                Row(
                    Column('email'), css_class='self-start w-full'
                ),
                Row(
                    Column('password'), css_class='self-start w-full'
                ),
                Row(
                    Column('confirm_password'), css_class='self-start w-full'
                ),
                Row(
                    Submit('submit', 'Register'), css_class='self-start w-full border border-gray-950 rounded rounded-md flex justify-center p-2 bg-green-500 arc-btn-retro'
                )
            )
        )

class EditUserProfile(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'johndoe'}))
    email = forms.EmailField(label='Email Address', widget=forms.TextInput(attrs={'placeholder': 'johndoe@gmail.com'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_layout(
            Layout(
                Row(
                    Column('username'), css_class='self-start w-full',
                ),
                Row(
                    Column('email'), css_class='self-start w-full',
                ),
                Row(
                     Submit('submit', 'Update profile'), css_class='self-start w-full border border-gray-950 rounded rounded-md flex justify-center p-2 cursor-pointer bg-green-500 arc-btn-retro'
                )
            )
        )