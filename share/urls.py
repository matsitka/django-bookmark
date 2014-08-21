from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from mpv import views
from accounts import views



from mpv.views import TagList, error404
from mpv.models import Share

import autocomplete_light
# import every app/autocomplete_light_registry.py
autocomplete_light.autodiscover()


from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',

    url(r'^autocomplete/', include('autocomplete_light.urls')),

    url(r'^(?P<link_random>\w{10})/$', 'mpv.views.share_id', name='share_id'),


    #django
    url(r'^$', 'mpv.views.index', name="home_list"),


    url(r'^tag/(?P<tag>[a-zA-Z0-9_.-]+)/$', 'mpv.views.TagList', name='tag_list'),
    url(r'^tag_all/$', 'mpv.views.allTags', name='all_tags'),


    #angular
    url(r'^angular/$', 'mpv.views.all_angular', name='all_share_angular'),

    #admin
    url(r'^admin/', include(admin.site.urls)),

    #add new post
    url(r'^', include('new.urls')),

    #api
    url(r'^api/', include('api.urls')),


    ##accounts
    url(r'^login/', views.sign_in, name='sign_in'),
    url(r'^sign_out/', views.sign_out, name='sign_out'),
    url(r'^register/', views.register, name='register'),



) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "mpv.views.error404"