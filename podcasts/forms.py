from django import forms
from .models import Podcast
from django.contrib.auth import get_user_model

User = get_user_model()

class PodcastAddForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = [
            'title',
            'description',
            'url',
            'favorite_episode',
            'saved_clip',
            'shownotes'
        ]

    # def clean_title(self):
    #     title = self.cleaned_data.get("title")
    #     title = title.capitalize()
    #     return title


class PodcastUpdateForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = [
            'description',
            'url',
            'logo',
            'favorite_episode',
            'saved_clip',
            'shownotes'
        ]

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
