from django.contrib import admin

from .models import Buss_Schedule,Sit,NewUser
# Register your models here.
admin.site.register(Buss_Schedule)
admin.site.register(Sit)
admin.site.register(NewUser)
