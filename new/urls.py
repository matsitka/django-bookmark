from django.conf.urls import patterns, url, include

from new import views


new_urls = patterns('',
    url(r'^/text/$', views.share_text, name='new-text'),
    url(r'^/link/$', views.share_link, name='new-link'),
    url(r'^/photo/$', views.share_photo, name='new-photo'),
    #url(r'^$', UserList.as_view(), name='user-list')
)


urlpatterns = patterns('',
    url(r'^new', include(new_urls)),

)