from django.contrib import admin
from .models import *
admin.site.site_header = 'Pizza My Mind Admin'
admin.site.site_title = 'Pizza My Mind Admin'
# Register your models here.
admin.site.register(Thursday)
admin.site.register(Company)
