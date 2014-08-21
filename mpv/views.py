from django.shortcuts import render, render_to_response, get_object_or_404, redirect, get_list_or_404
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect

from mpv.models import Share, Text, Link
from accounts.models import User
from mpv.models import models
from taggit.models import Tag, TaggedItem
from accounts.forms import SigninForm, UserForm

from django.views.generic import TemplateView, ListView
import string
import random
from django.shortcuts import render, render_to_response

from django.template import RequestContext
#https://docs.djangoproject.com/en/dev/ref/class-based-views/generic-display/#listview

#login, registration on index
from django.db import transaction
from django.db import IntegrityError

from accounts.views import sign_in


def index(request):

    uid = request.session.get('user')

    #if user not connected
    if uid is None:

        return sign_in(request)



    #if user connected

    else:
        usr = User.get_by_id(uid)
        #shares = Share.objects.all().order_by('-created_at')
        shares = usr.shares.all().order_by('-created_at')

        return render_to_response('accounts/index_connected.html', {
            'user':usr,
            'share_list': shares
        }, context_instance=RequestContext(request),)


def TagList(request, tag):

    uid = request.session.get('user')

    #if user not connected
    if uid is None:
    #if not request.user.is_authenticated():

        return sign_in(request)

    else:

        uid = request.session.get('user')

        usr = User.get_by_id(uid)


    ## retrieve tags slug based on user
        shares = usr.shares.filter(taggit__slug=tag).order_by('-created_at')

    #shares = Share.objects.filter(taggit__name=tag, author=user).select_related().get()




        return render_to_response('tag_list.html', {
            'user':usr,
            'tag_list': shares
        }, context_instance=RequestContext(request),)


def share_id(request, link_random):

    uid = request.session.get('user')

    #if user not connected
    if uid is None:
    #if not request.user.is_authenticated():

        return sign_in(request)

    else: #if user is connected


        try:
            user = User.objects.select_related().get(pk=request.session.get('user'))

        except User.DoesNotExist:
            user = None
            raise Http404
            #user = None

        #shares = Share.objects.all().order_by('-created_at')
        #shares = usr.shares.get(random=link_random)

        try:

            #shares = get_object_or_404(Share, random=link_random)
            share = Share.objects.filter(random=link_random, author=user).select_related().get()
        except Share.DoesNotExist:
            raise Http404



        return render(request, 'share_details.html', {
            'share_details': share,
            'user': user
        })



def all_angular(request): #angular


    return render(request, 'all_share_angular.html', {

    })

def error404(request):
    return render(request,'404.html', status=404)


def allTags(request):

    uid = request.session.get('user')

    #if user not connected
    if uid is None:
    #if not request.user.is_authenticated():


        return sign_in(request)


    else:

        uid = request.session.get('user')

        usr = User.get_by_id(uid)



    ## retrieve all tags slug based on user
        all_tags = Tag.objects.filter(share__author=usr).order_by('-tag_count').annotate(tag_count=models.Count('share'))




        return render_to_response('all_tags.html', {
            'user':usr,
            'all_tags': all_tags,
           # 'shares': shares
        }, context_instance=RequestContext(request),)

