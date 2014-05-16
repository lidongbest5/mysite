from django.contrib import admin
from blog.models import *

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Saying)
admin.site.register(SayingComment)
admin.site.register(SayingFavourite)
