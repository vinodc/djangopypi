import os
import re

from django.conf import settings
from django.db import transaction
from django.http import *
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import MultiValueDict
from django.contrib.auth import login

from djangopypi.decorators import basic_auth
from djangopypi.forms import PackageForm, ReleaseForm
from djangopypi.models import Package, Release, Distribution, Classifier



ALREADY_EXISTS_FMT = _(
    "A file named '%s' already exists for %s. Please create a new release.")

def submit_package_or_release(user, post_data, files):
    """Registers/updates a package or release"""
    try:
        package = Package.objects.get(name=post_data['name'])
        if user not in package.owners.all():
            return HttpResponseForbidden(
                    "That package is owned by someone else!")
    except Package.DoesNotExist:
        package = None

    package_form = PackageForm(post_data, instance=package)
    if package_form.is_valid():
        package = package_form.save(commit=False)
        package.owner = user
        package.save()
        for c in post_data.getlist('classifiers'):
            classifier, created = Classifier.objects.get_or_create(name=c)
            package.classifiers.add(classifier)
        if files:
            allow_overwrite = getattr(settings,
                "DJANGOPYPI_ALLOW_VERSION_OVERWRITE", False)
            try:
                release = Release.objects.get(version=post_data['version'],
                                              package=package,
                                              distribution=UPLOAD_TO + '/' +
                                              files['distribution']._name)
                if not allow_overwrite:
                    return HttpResponseForbidden(ALREADY_EXISTS_FMT % (
                                release.filename, release))
            except Release.DoesNotExist:
                release = None

            # If the old file already exists, django will append a _ after the
            # filename, however with .tar.gz files django does the "wrong"
            # thing and saves it as package-0.1.2.tar_.gz. So remove it before
            # django sees anything.
            release_form = ReleaseForm(post_data, files, instance=release)
            if release_form.is_valid():
                if release and os.path.exists(release.distribution.path):
                    os.remove(release.distribution.path)
                release = release_form.save(commit=False)
                release.package = package
                release.save()
            else:
                return HttpResponseBadRequest(
                        "ERRORS: %s" % release_form.errors)
    else:
        return HttpResponseBadRequest("ERRORS: %s" % package_form.errors)

    return HttpResponse()

@basic_auth
@transaction.commit_manually
def register_or_upload(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only post requests are supported')
    
    name = request.POST.get('name',None).strip()
    
    if not name:
        return HttpResponseBadRequest('No package name specified')
    
    try:
        package = Package.objects.get(name=name)
    except Package.DoesNotExist:
        package = Package.objects.create(name=name)
        package.owners.add(request.user)
    
    if (request.user not in package.owners.all() and 
        request.user not in package.maintainers.all()):
        
        return HttpResponseForbidden('You are not an owner/maintainer of %s' % (package.name,))
    
    version = request.POST.get('version',None).strip()
    metadata_version = request.POST.get('metadata_version', None).strip()
    
    if not version or not metadata_version:
        transaction.rollback()
        return HttpResponseBadRequest('Release version and metadata version must be specified')
    
    if not metadata_version in settings.DJANGOPYPI_METADATA_FIELDS:
        transaction.rollback()
        return HttpResponseBadRequest('Metadata version must be one of: %s' 
                                      (', '.join(settings.DJANGOPYPI_METADATA_FIELDS.keys()),))
    
    release, created = Release.objects.get_or_create(package=package,
                                                     version=version)
    
    if (('classifiers' in request.POST or 'download_url' in request.POST) and 
        metadata_version == '1.0'):
        metadata_version = '1.1'
    
    release.metadata_version = metadata_version
    
    fields = settings.DJANGOPYPI_METADATA_FIELDS[metadata_version]
    
    if 'classifiers' in request.POST:
        request.POST.setlist('classifier',request.POST.getlist('classifiers'))
    
    release.package_info = MultiValueDict(dict(filter(lambda t: t[0] in fields,
                                                      request.POST.iterlists())))
    
    for key, value in release.package_info.iterlists():
        release.package_info.setlist(key,
                                     filter(lambda v: v != 'UNKNOWN', value))
    
    release.save()
    if not 'content' in request.FILES:
        transaction.commit()
        return HttpResponse('release registered')
    
    uploaded = request.FILES.get('content')

    delete_dists = []
    for dist in release.distributions.all():
        if os.path.basename(dist.content.name) == uploaded.name:
            if settings.DJANGOPYPI_ALLOW_VERSION_OVERWRITE:
                delete_dists.append(dist)
            else:
                transaction.rollback()
                return HttpResponseBadRequest('That file has already been uploaded...')
    
    if len(delete_dists) != 0:
        for dist in delete_dists:
            # Remove file.
            dist.content.delete()
            # Remove entry.
            dist.delete()
            
    md5_digest = request.POST.get('md5_digest','')
    
    try:
        new_file = Distribution.objects.create(release=release,
                                               content=uploaded,
                                               filetype=request.POST.get('filetype','sdist'),
                                               pyversion=request.POST.get('pyversion',''),
                                               uploader=request.user,
                                               comment=request.POST.get('comment',''),
                                               signature=request.POST.get('gpg_signature',''),
                                               md5_digest=md5_digest)
    except Exception, e:
        transaction.rollback()
        print str(e)
    
    transaction.commit()
    
    return HttpResponse('upload accepted')

def list_classifiers(request, mimetype='text/plain'):
    response = HttpResponse(mimetype=mimetype)
    response.write(u'\n'.join(map(lambda c: c.name,Classifier.objects.all())))
    return response
