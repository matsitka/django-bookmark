from django import forms
from django.contrib.auth.models import UserManager
from mpv.models import Share, Text, Link, Photo

from accounts.models import User

#autocomplete-lights
import autocomplete_light
from autocomplete_light.contrib import taggit_tagfield


#class ShareForm(forms.ModelForm):
class TextForm(forms.ModelForm):


    comment = forms.CharField(widget=forms.Textarea(attrs = {'class': 'first-top'}), initial='Add a comment...')

    ## autocomplete-light
    taggit = taggit_tagfield.TagField(widget=taggit_tagfield.TagWidget('TagAutocomplete'), required=False)

    #author = forms.CharField(widget=forms.HiddenInput(), required=True)
    created_at = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    def randomString():
        um = UserManager()
        return um.make_random_password(length=10)

    random = forms.CharField(max_length=10, initial=randomString, widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Text
        exclude = ('author',)
        widgets = {
            'taggit': autocomplete_light.TextWidget('TagAutocomplete'),
        }



        #order the forms field http://stackoverflow.com/a/5747259/2942942
    def __init__(self, *args, **kwargs):
        #self.author = user #http://stackoverflow.com/a/5122029/2942942

        super(TextForm, self).__init__(*args, **kwargs)


        self.fields.keyOrder = [

        'comment',
        'taggit']




class LinkForm(forms.ModelForm):  #http://stackoverflow.com/a/606318


    url = forms.CharField(max_length=200, widget=forms.TextInput(attrs = {'class': 'first-top', 'placeholder': 'URL'}))

    comment = forms.CharField(widget=forms.Textarea(), initial='Add a comment...')

    ## autocomplete-light
    taggit = taggit_tagfield.TagField(widget=taggit_tagfield.TagWidget('TagAutocomplete'), required=False)


    created_at = forms.DateTimeField(widget=forms.HiddenInput(), required=False)


    def randomString():
        um = UserManager()
        return um.make_random_password(length=10)

    random = forms.CharField(max_length=10, initial=randomString, widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Link
        exclude = ('author',)
        widgets = {
            'taggit': autocomplete_light.TextWidget('TagAutocomplete'),

        }


    #order the forms field http://stackoverflow.com/a/5747259/2942942
    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [

        'url',
        #'title',
        'comment',
        'taggit']



class PhotoForm(forms.ModelForm):  #http://stackoverflow.com/a/606318

    image_original = forms.ImageField(widget=forms.FileInput(attrs = {'class': 'first-top'}), required=False)
    comment = forms.CharField(widget=forms.Textarea(), initial='Add a comment...')

    ## autocomplete-light
    taggit = taggit_tagfield.TagField(widget=taggit_tagfield.TagWidget('TagAutocomplete'), required=False)

    created_at = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    image_crop = forms.ImageField(widget=forms.HiddenInput(), required=False)

    def randomString():
        um = UserManager()
        return um.make_random_password(length=10)

    random = forms.CharField(max_length=10, initial=randomString, widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Photo
        exclude = ('author',)
        widgets = {
            'taggit': autocomplete_light.TextWidget('TagAutocomplete'),
        }

        #order the forms field http://stackoverflow.com/a/5747259/2942942
    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [

        'image_original',
        #'title',
        'comment',
        'taggit']

