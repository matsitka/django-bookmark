from django import template
from django.db import models
register = template.Library()

from mpv.models import Share, Tagged
from accounts.models import User



def show_stats():


    user = User.objects.all()
    shares = Share.objects.all()


    return {
        'user': user,
        'shares': shares
    }

register.inclusion_tag('template_tags/stats.html')(show_stats)