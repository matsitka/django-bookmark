from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from mpv.models import Share, Text, Link, Photo, Tagged
from accounts.models import User


class ShareAdmin(admin.ModelAdmin):
    pass

    list_display = ('created_at', 'random')

admin.site.register(Share, ShareAdmin)
#admin.site.register(User)

#admin.site.register(Share)

admin.site.register(Text)
admin.site.register(Link)
admin.site.register(Photo)
admin.site.register(Tagged)



admin.site.register(User)

