from django import forms
from .models import Podcast

class PodcastAddForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = [
            'title',
            'description',
            'url',
            'favorite_episode',
            'saved_clips1',
            'shownotes'
        ]

class PodcastUpdateForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = [
            'description',
            'url',
            'favorite_episode',
            'saved_clips1',
            'shownotes'
        ]
