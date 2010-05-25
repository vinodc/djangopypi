from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import list_detail



from djangopypi.models import Project, Release
from djangopypi.http import HttpResponseNotImplemented
from djangopypi.http import parse_distutils_request
from djangopypi.views.dists import register_or_upload
from djangopypi.views.users import create_user
from djangopypi.views.search import search



def root(request, fallback_view=None, **kwargs):
    """ Root view of the package index, handle incoming actions from distutils
    or redirect to a more user friendly view """
    
    if request.method != 'POST':
        if fallback_view is None:
            fallback_view = settings.DJANGOPYPI_FALLBACK_VIEW
        return fallback_view(request, **kwargs)
    
    parse_distutils_request(request)
    print str(request.POST)
    action = request.POST.get(':action','')
    
    if not action in settings.DJANGOPYPI_ACTION_VIEWS:
        print 'unknown action: %s' % (action,)
        return HttpResponseNotImplemented("The action %s is not implemented" % (action,))
    
    return settings.DJANGOPYPI_ACTION_VIEWS[action](request, **kwargs)




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
