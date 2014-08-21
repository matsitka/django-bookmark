from django import template
from django.db import models
register = template.Library()

from mpv.models import Share, Tagged
from accounts.models import User
from taggit.models import Tag, TaggedItem

from django.template import RequestContext

#http://stackoverflow.com/a/2160298/2942942
@register.inclusion_tag('template_tags/tags.html', takes_context = True)
def show_tags(context):
    request = context['request']
    uid = request.session['user']

    user = User.get_by_id(uid)



    ### filter by user, then annotate (regroup), and count the last 10 tags
    tagged = Tag.objects.filter(share__author=user).order_by('-tag_count').annotate(tag_count=models.Count('share'))[:10]


    all_tags = Tag.objects.filter(share__author=user)

    ### get all the last 5 shares
    #tagged = user.shares.all().order_by('-created_at')[:5]




    return {
        'tagged_items': tagged,
        'all_tags' : all_tags
    }


