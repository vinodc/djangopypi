from django.views.generic import list_detail, create_update
from django.db.models.query import Q

from djangopypi.decorators import user_owns_package, user_maintains_package
from djangopypi.models import Package
from djangopypi.forms import SimplePackageSearchForm, PackageForm



def index(request, **kwargs):
    kwargs.setdefault('template_object_name','package')
    kwargs.setdefault('queryset',Package.objects.all())
    return list_detail.object_list(request, **kwargs)

def details(request, package, **kwargs):
    kwargs.setdefault('template_object_name','package')
    kwargs.setdefault('queryset',Package.objects.all())
    return list_detail.object_detail(request, object_id=package, **kwargs)

def doap(request, package, **kwargs):
    kwargs.setdefault('template_name','djangopypi/package_doap.xml')
    kwargs.setdefault('mimetype', 'text/xml')
    return details(request, package, **kwargs)

def search(request, **kwargs):
    if request.method == 'POST':
        form = SimplePackageSearchForm(request.POST)
    else:
        form = SimplePackageSearchForm(request.GET)
    
    if form.is_valid():
        q = form.cleaned_data['query']
        kwargs['queryset'] = Package.objects.filter(Q(name__contains=q) | 
                                                    Q(releases__package_info__contains=q)).distinct()
    return index(request, **kwargs)

@user_owns_package()
def manage(request, package, **kwargs):
    kwargs['object_id'] = package
    kwargs.setdefault('form_class', PackageForm)
    kwargs.setdefault('template_name', 'djangopypi/package_manage.html')
    kwargs.setdefault('template_object_name', 'package')
    
    return create_update.update_object(request, **kwargs)
