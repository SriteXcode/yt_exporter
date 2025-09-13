from django import forms

class PlaylistForm(forms.Form):
    playlist_url = forms.URLField(label='Playlist URL', widget=forms.URLInput(attrs={
        'class': 'form-control', 'placeholder': 'https://www.youtube.com/playlist?list=...'
    }))
    limit = forms.IntegerField(label='Max videos (optional)', required=False, min_value=1, widget=forms.NumberInput({
        'class': 'form-control', 'placeholder': 'Leave empty for all'
    }))
