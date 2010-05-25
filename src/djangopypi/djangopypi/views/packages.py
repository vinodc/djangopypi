from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import list_detail
from django.shortcuts import get_object_or_404


from djangopypi.models import Project, Release
from djangopypi.views import release as release_views



def index(request, **kwargs):
    kwargs.setdefault('template_object_name','project')
    return list_detail.object_list(request, queryset=Project.objects.all(),
                                   **kwargs)

def details(request, project, **kwargs):
    kwargs.setdefault('template_object_name','project')
    return list_detail.object_detail(request, queryset=Project.objects.all(),
                                     object_id=project, **kwargs)