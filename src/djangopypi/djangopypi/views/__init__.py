from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from djangopypi.models import Project, Release
from djangopypi.http import HttpResponseNotImplemented
from djangopypi.http import parse_distutils_request
from djangopypi.views.dists import register_or_upload
from djangopypi.views.users import create_user
from djangopypi.views.search import search



def root(request, root_redirect=None, **kwargs):
    if request.method != 'POST':
        if root_redirect is None:
            root_redirect = reverse(settings.DJANGOPYPI_SIMPLE_VIEW)
        return HttpResponseRedirect(root_redirect)
   
    parse_distutils_request(request)
    
    action = request.POST.get(':action','')
    
    if not action in settings.DJANGOPYPI_ACTION_VIEWS:
        return HttpResponseNotImplemented("The action %s is not implemented" % (action,))
    
    return settings.DJANGOPYPI_ACTION_VIEWS(request, **kwargs)


def simple(request, template_name="djangopypi/simple.html"):
    context = RequestContext(request, {
        "dists": Project.objects.all().order_by("name"),
        "title": 'Package Index',
    })

    return render_to_response(template_name, context_instance=context)


def show_links(request, dist_name,
        template_name="djangopypi/show_links.html"):
    try:
        project = Project.objects.get(name=dist_name)
        releases = project.releases.all().order_by('-version')
    except Project.DoesNotExist:
        raise Http404

    context = RequestContext(request, {
        "dist_name": dist_name,
        "releases": releases,
        "project": project,
        "title": project.name,
    })

    return render_to_response(template_name, context_instance=context)


def show_version(request, dist_name, version,
        template_name="djangopypi/show_version.html"):
    try:
        project = Project.objects.get(name=dist_name)
        release = project.releases.get(version=version)
    except (Project.DoesNotExist, Release.DoesNotExist):
        raise Http404()

    context = RequestContext(request, {
        "dist_name": dist_name,
        "version": version,
        "release": release,
        "title": dist_name,
    })

    return render_to_response(template_name, context_instance=context)
