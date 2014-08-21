from django.conf.urls import patterns, url, include

from .api import UserList, UserDetail, LinkDetail, ShareLinkList
from .api import ShareList, ShareDetail, UserShareList, LinkList

user_urls = patterns('',
    #url(r'^/(?P<username>[0-9a-zA-Z_-]+)/shares$', UserShareList.as_view(), name='usershare-list'),
    #url(r'^/(?P<username>[0-9a-zA-Z_-]+)$', UserDetail.as_view(), name='user-detail'),
    url(r'^/(?P<name>[0-9a-zA-Z_-]+)/shares$', UserShareList.as_view(), name='usershare-list'),
    url(r'^/(?P<name>[0-9a-zA-Z_-]+)$', UserDetail.as_view(), name='user-detail'),
    url(r'^$', UserList.as_view(), name='user-list')
)

share_urls = patterns('',

    url(r'^/(?P<pk>\d+)/links$', ShareLinkList.as_view(), name='sharelink-list'),

    #url(r'^/(?P<pk>\d+)/tags$', TagList.as_view(), name='tag-list'),
    url(r'^/(?P<pk>\d+)$', ShareDetail.as_view(), name='share-detail'),
    url(r'^$', ShareList.as_view(), name='share-list')
)


link_urls = patterns('',
    url(r'^/(?P<pk>\d+)$', LinkDetail.as_view(), name='link-detail'),
    url(r'^$', LinkList.as_view(), name='link-list')
)


urlpatterns = patterns('',
    url(r'^users', include(user_urls)),
    url(r'^shares', include(share_urls)),

    url(r'^links', include(link_urls)),
)