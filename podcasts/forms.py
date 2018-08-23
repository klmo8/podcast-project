from django import forms
from .models import Podcast
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)

User = get_user_model()

class PodcastAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PodcastAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    helper = FormHelper()
    helper.form_class = 'form_horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'

    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 3}))
    class Meta:
        model = Podcast
        fields = [
            'title',
            'description',
            'url',
            # 'logo',
            'favorite_episode',
            'saved_clip',
            'shownotes',
        ]
        labels = {
            # 'logo': 'Link to iTunes Coverart',
            'url': 'Homepage',
        }



class PodcastUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PodcastUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    helper = FormHelper()
    helper.form_class = 'form_horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'

    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 3}))
    class Meta:
        model = Podcast
        fields = [
            'title',
            'description',
            'url',
            'logo',
            'favorite_episode',
            'saved_clip',
            'shownotes',
        ]
        labels = {
            'logo': 'Link to iTunes Coverart',
            'url': 'Homepage',
        }

class PodcastDeleteForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = []

class RegisterUserForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = "The two password fields didn't match."
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages
            )
        return password2

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
