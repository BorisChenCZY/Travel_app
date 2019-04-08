from django import forms
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE
from django.contrib.flatpages.models import FlatPage

TYPES = [
	(1, '导览文章'),
	(2, '商城'),
]
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100)
    audio_title = forms.CharField(required=False, max_length=100)
    file = forms.FileField(required=False)
    image = forms.FileField()
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 10, 'rows': 30}))
    brief = forms.CharField(widget=forms.Textarea(attrs={'style' : 'width:100%; height:10%'}))
    type = forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=TYPES))
    edit_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = FlatPage

    # def __init__(self, *argv, **argc):
        # edit_id.widget = forms.HiddenInput()
