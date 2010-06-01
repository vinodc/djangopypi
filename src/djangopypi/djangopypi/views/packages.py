from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import list_detail
from django.shortcuts import get_object_or_404


from djangopypi.models import Package



def index(request, **kwargs):
    print str(request.GET)
    kwargs.setdefault('template_object_name','package')
    kwargs.setdefault('queryset',Package.objects.all())
    return list_detail.object_list(request, **kwargs)

def details(request, package, **kwargs):
    kwargs.setdefault('template_object_name','package')
    kwargs.setdefault('queryset',Package.objects.all())
    return list_detail.object_detail(request, object_id=package, **kwargs)

def search(request):
    return None