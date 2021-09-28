from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import *

admin.site.register(User)
admin.site.register(Pays)
admin.site.register(Notes)
admin.site.register(Templates)
