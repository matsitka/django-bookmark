from django.shortcuts import render


from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from accounts.forms import SigninForm, UserForm
from accounts.models import User
import share.settings as settings

import datetime
from django.db import transaction

def sign_in(request):
    user = None
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
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

def sign_out(request):
    del request.session['user']
    return HttpResponseRedirect('/')

def register(request):
    user = None
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            #https://github.com/realpython/book3-exercises/blob/7dce6dbf77c62124cb0ef6d909cdd1a1afdc88de/django_ecommerce/payments/views.py
            cd = form.cleaned_data

            try:
                with transaction.atomic():
                    user = User.create(cd['name'], cd['email'], cd['password'])
                    user.save()
            except IntegrityError:
                form.addError(cd['email'] + ' is already a member')
            else:
                request.session['user'] = user.pk
                return HttpResponseRedirect('/')


            #user = User(
                #name=form.cleaned_data['name'],
            #    email=form.cleaned_data['email'],
            #)
            #ensure encrpyted password
            #user.set_password(form.cleaned_data['password'])

            #try:
            #    user.save()
            #except IntegrityError:
            #    form.addError(user.email + ' is already a member')
            #else:
            #    request.session['user'] = user.pk
            #    return HttpResponseRedirect('/')

    else:

        form = UserForm()

    return render_to_response(
        'accounts/register.html',
        {
          'form': form,
          'user': user,
        },
        context_instance=RequestContext(request)
    )