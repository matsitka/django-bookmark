from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect

from mpv.models import Share, Text, Link
from mpv.models import models
from new.forms import TextForm, LinkForm, PhotoForm

#accounts
from accounts.forms import SigninForm
from accounts.models import User
from django.contrib.auth.decorators import login_required

from django.forms.models import inlineformset_factory

#dragImage
import os



# Create your views here.

def share_text(request):
    #http://stackoverflow.com/questions/8466768/using-request-user-with-django-modelform

    uid = request.session.get('user')

    #if user not connected
    if uid is None:

        #not connected
        user = None


        if request.method == 'POST':

            #author = Share(user=request.user)

            form = SigninForm(request.POST)
            if form.is_valid():

                #form.author = request.user


                results = User.objects.filter(email=form.cleaned_data['email'])
                if len(results) == 1:
                    if results[0].check_password(form.cleaned_data['password']):
                        request.session['user'] = results[0].pk
                        return HttpResponseRedirect('/')
                    else:
                        form.addError('Incorrect email address or password')
                else:
                    form.addError('Incorrect email address or password')
        else:
            form = SigninForm()

        print form.non_field_errors()

        return render_to_response(
            'accounts/sign_in.html',
            {
                'form': form,
                'user': user
            },
            context_instance=RequestContext(request)
        )

    else: #if user is connected


        uid = request.session.get('user')
        user = User.get_by_id(uid)

        if request.method == "POST":

                #text = Share(author=request.user)

                form = TextForm(request.POST)
                if form.is_valid():


                    #load tags
                    taggit = form.cleaned_data['taggit']

                    text = form.save(commit=False)

                    #save the user instance
                    text.author = user

                    text.save()

                    #save/add tags in text object #http://stackoverflow.com/questions/5359714/django-django-taggit-form
                    for taggit in taggit:
                        text.taggit.add(taggit)

                    last_random = Share.objects.values_list('random', flat=True).order_by('-created_at')[:1]
                    #this returns [u'5eXB612345']

                    #return the random sequence only to a strng format 5eXB6
                    new_random = str(last_random)[3:13]



                    return redirect('/%s' % new_random)


        else:
            form = TextForm()


        return render_to_response(
            'new/text.html',
            {
                'text_form': form,
                'user': user
            },
            context_instance=RequestContext(request)
        )



def share_link(request):

    uid = request.session.get('user')

    #if user not connected
    if uid is None:

        #not connected
        user = None


        if request.method == 'POST':

            #author = Share(user=request.user)

            form = SigninForm(request.POST)
            if form.is_valid():

                #form.author = request.user


                results = User.objects.filter(email=form.cleaned_data['email'])
                if len(results) == 1:
                    if results[0].check_password(form.cleaned_data['password']):
                        request.session['user'] = results[0].pk
                        return HttpResponseRedirect('/')
                    else:
                        form.addError('Incorrect email address or password')
                else:
                    form.addError('Incorrect email address or password')
        else:
            form = SigninForm()

        print form.non_field_errors()

        return render_to_response(
            'accounts/sign_in.html',
            {
                'form': form,
                'user': user
            },
            context_instance=RequestContext(request)
        )

    else: #if user is connected


        uid = request.session.get('user')
        user = User.get_by_id(uid)

        if request.method == "POST":

                #text = Share(author=request.user)

                form = LinkForm(request.POST)
                if form.is_valid():

                    #load tags
                    taggit = form.cleaned_data['taggit']

                    link = form.save(commit=False)

                    #save the user instance
                    link.author = user

                    link.save()

                    #save/add tags in text object #http://stackoverflow.com/questions/5359714/django-django-taggit-form
                    for taggit in taggit:
                        link.taggit.add(taggit)

                    last_random = Share.objects.values_list('random', flat=True).order_by('-created_at')[:1]
                    #this returns [u'5eXB612345']

                    #return the random sequence only to a strng format 5eXB6
                    new_random = str(last_random)[3:13]



                    return redirect('/%s' % new_random)


        else:
            form = LinkForm()



        return render_to_response(
            'new/link.html',
            {
                'link_form': form,
                'user': user
            },
            context_instance=RequestContext(request)
        )



def share_photo(request):

    uid = request.session.get('user')

    #if user not connected
    if uid is None:

        #not connected
        user = None


        if request.method == 'POST':

            #author = Share(user=request.user)

            form = SigninForm(request.POST)
            if form.is_valid():

                #form.author = request.user


                results = User.objects.filter(email=form.cleaned_data['email'])
                if len(results) == 1:
                    if results[0].check_password(form.cleaned_data['password']):
                        request.session['user'] = results[0].pk
                        return HttpResponseRedirect('/')
                    else:
                        form.addError('Incorrect email address or password')
                else:
                    form.addError('Incorrect email address or password')
        else:
            form = SigninForm()

        print form.non_field_errors()

        return render_to_response(
            'accounts/sign_in.html',
            {
                'form': form,
                'user': user
            },
            context_instance=RequestContext(request)
        )

    else: #if user is connected

        uid = request.session.get('user')
        user = User.get_by_id(uid)

        if request.method == "POST":

                #text = Share(author=request.user)

                form = PhotoForm(request.POST, request.FILES)
                if form.is_valid():

                    #load tags
                    taggit = form.cleaned_data['taggit']

                    photo = form.save(commit=False)

                    #save the user instance
                    photo.author = user

                    photo.save()

                    #save/add tags in text object #http://stackoverflow.com/questions/5359714/django-django-taggit-form
                    for taggit in taggit:
                        photo.taggit.add(taggit)

                    last_random = Share.objects.values_list('random', flat=True).order_by('-created_at')[:1]
                    #this returns [u'5eXB612345']

                    #return the random sequence only to a strng format 5eXB6
                    new_random = str(last_random)[3:13]



                    return redirect('/%s' % new_random)


        else:
            form = PhotoForm()



        return render_to_response(
            'new/photo.html',
            {
                'photo_form': form,
                'user': user
            },
            context_instance=RequestContext(request)
        )




