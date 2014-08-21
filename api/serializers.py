
from rest_framework import serializers

from mpv.models import Share, Link
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    #posts = serializers.HyperlinkedIdentityField('shares', view_name='usershare-list', lookup_field='username')
    posts = serializers.HyperlinkedIdentityField('shares', view_name='usershare-list', lookup_field='name')

    class Meta:
        model = User
        fields = ('id', 'name', 'shares',)


class ShareSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    #links = serializers.HyperlinkedIdentityField('links', view_name='sharelink-list')

    def get_validation_exclusions(self):
        # Need to exclude `author` since we'll add that later based off the request
        exclusions = super(ShareSerializer, self).get_validation_exclusions()
        return exclusions + ['author']

    class Meta:
        model = Share




class LinkSerializer(serializers.ModelSerializer):
    link = serializers.Field('url')

    class Meta:
        model = Link