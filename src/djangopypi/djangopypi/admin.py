from django.contrib import admin
from djangopypi.models import *

admin.site.register(Package)
admin.site.register(Release)
admin.site.register(Classifier)
admin.site.register(File)
admin.site.register(Review)
