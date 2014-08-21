from rest_framework import generics, permissions


from .serializers import UserSerializer, ShareSerializer, LinkSerializer
from mpv.models import Share, Link
from accounts.models import User

class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    #lookup_field = 'username'
    lookup_field = 'name'

    """
    def get_queryset(self):
        queryset = super(UserDetail, self).get_queryset()
        return queryset.filter(users__username=self.kwargs.get('username'))
    """

class ShareMixin(object):
    model = Share
    serializer_class = ShareSerializer


    def pre_save(self, obj):
        """Force author to the current user on save"""
        obj.author = self.request.user
        return super(ShareMixin, self).pre_save(obj)


class ShareList(ShareMixin, generics.ListCreateAPIView):
    pass


class ShareDetail(ShareMixin, generics.RetrieveUpdateDestroyAPIView):
    pass

class UserShareList(generics.ListAPIView):
    model = Share
    serializer_class = ShareSerializer

    #def get_queryset(self):
    #    queryset = super(UserShareList, self).get_queryset()
    #    return queryset.filter(author__username=self.kwargs.get('username'))


class LinkList(generics.ListCreateAPIView):
    model = Link
    serializer_class = LinkSerializer


class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Link
    serializer_class = LinkSerializer

class ShareLinkList(generics.ListAPIView):
    model = Link
    serializer_class = LinkSerializer

    def get_queryset(self):
        queryset = super(ShareLinkList, self).get_queryset()
        return queryset.filter(share_ptr__pk=self.kwargs.get('pk'))

