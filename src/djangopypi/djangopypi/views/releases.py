from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import list_detail
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from djangopypi.models import Package, Release



def index(request, **kwargs):
    print str(request)
    kwargs.setdefault('template_object_name','release')
    kwargs.setdefault('queryset',Release.objects.all())
    return list_detail.object_list(request, **kwargs)

def details(request, package, version, **kwargs):
    kwargs.setdefault('template_object_name','release')
    kwargs.setdefault('template_name','djangopypi/release_detail.html')
    kwargs.setdefault('extra_context',{})
    
    release = get_object_or_404(Package, name=package).get_release(version)
    
    if not release:
        return Http404()
    
    kwargs['extra_context'][kwargs['template_object_name']] = release
        
    return render_to_response(kwargs['template'], kwargs['extra_context'],
                              context_instance=RequestContext(request))

def doap(request, package, version, **kwargs):
    kwargs.setdefault('template_name','djangopypi/release_doap.xml')
    return details(request, package, version, **kwargs)