from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import list_detail
from django.shortcuts import get_object_or_404


from djangopypi.models import Project



def index(request, **kwargs):
    kwargs.setdefault('template_object_name','project')
    kwargs.setdefault('queryset',Project.objects.all())
    return list_detail.object_list(request, **kwargs)

def details(request, project, **kwargs):
    kwargs.setdefault('template_object_name','project')
    kwargs.setdefault('queryset',Project.objects.all())
    return list_detail.object_detail(request, object_id=project, **kwargs)