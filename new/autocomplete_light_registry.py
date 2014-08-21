import autocomplete_light
from taggit.models import Tag

from mpv.models import Share

#accounts
from accounts.models import User
#from django.template import RequestContext, request
# This will generate a ShareAutocomplete class



#http://stackoverflow.com/a/19321304/2942942
class TagAutocomplete(autocomplete_light.AutocompleteModelBase):

    #search_fields = ['slug']

    autocomplete_js_attributes={'placeholder': 'Search or add seperated-comma tag',}


    #select tag per user
    def choices_for_request(self):

        uid = self.request.session.get('user')
        user = User.get_by_id(uid)

        tag = Tag.objects.all()


        #regroup and filter by user
        self.choices = self.choices.annotate().filter(share__author=user)

        #choices = self.choices.filter(share__author=user)
        return super(TagAutocomplete, self).choices_for_request()



autocomplete_light.register(Tag, TagAutocomplete)

