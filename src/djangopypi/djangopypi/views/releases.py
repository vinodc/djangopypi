from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import list_detail, create_update
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from djangopypi.decorators import user_owns_package, user_maintains_package
from djangopypi.models import Package, Release
from djangopypi.forms import ReleaseForm



def index(request, **kwargs):
    kwargs.setdefault('template_object_name','release')
    kwargs.setdefault('queryset',Release.objects.filter(hidden=False))
    return list_detail.object_list(request, **kwargs)

def details(request, package, version, **kwargs):
    release = get_object_or_404(Package, name=package).get_release(version)
    
    if not release:
        return Http404()
    
    kwargs.setdefault('template_object_name','release')
    kwargs.setdefault('template_name','djangopypi/release_detail.html')
    kwargs.setdefault('extra_context',{})
    kwargs.setdefault('mimetype',settings.DEFAULT_CONTENT_TYPE)
    
    kwargs['extra_context'][kwargs['template_object_name']] = release
        
    return render_to_response(kwargs['template_name'], kwargs['extra_context'],
                              context_instance=RequestContext(request),
                              mimetype=kwargs['mimetype'])

def doap(request, package, version, **kwargs):
    kwargs.setdefault('template_name','djangopypi/release_doap.xml')
    kwargs.setdefault('mimetype', 'text/xml')
    return details(request, package, version, **kwargs)

@user_maintains_package()
def manage(request, package, version, **kwargs):
    release = get_object_or_404(Package, name=package).get_release(version)
    
    if not release:
        return Http404()
    
    kwargs['object_id'] = release.pk
    
    kwargs.setdefault('form_class', ReleaseForm)
    kwargs.setdefault('template_name', 'djangopypi/release_manage.html')
    kwargs.setdefault('template_object_name', 'release')
    
    return create_update.update_object(request, **kwargs)