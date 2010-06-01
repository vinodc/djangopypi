import os
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson as json
from django.utils.datastructures import MultiValueDict
from django.contrib.auth.models import User



class Classifier(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _(u"classifier")
        verbose_name_plural = _(u"classifiers")

    def __unicode__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    auto_hide = models.BooleanField(default=True, blank=False)
    allow_comments = models.BooleanField(default=True, blank=False)
    owners = models.ManyToManyField(User, blank=True,
                                    related_name="packages_owned")
    maintainers = models.ManyToManyField(User, blank=True,
                                         related_name="packages_maintained")
    
    class Meta:
        verbose_name = _(u"package")
        verbose_name_plural = _(u"packages")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('djangopypi-package-details', (), {'package': self.name})
    
    @property
    def latest(self):
        try:
            return self.releases.latest()
        except Release.DoesNotExist:
            return None
    
    def get_release(self, version):
        """Return the release object for version, or None"""
        try:
            return self.releases.get(version=version)
        except Release.DoesNotExist:
            return None

class Release(models.Model):
    package = models.ForeignKey(Package, related_name="releases")
    version = models.CharField(max_length=128)
    metadata_version = models.CharField(max_length=64, default='1.0')
    package_info = models.TextField(blank=False)
    hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        verbose_name = _(u"release")
        verbose_name_plural = _(u"releases")
        unique_together = ("package", "version")
        get_latest_by = 'created'
        ordering = ['-created']

    def __unicode__(self):
        return self.release_name
    
    @property
    def release_name(self):
        return u"%s-%s" % (self.package.name, self.version)
    
    @property
    def parsed_package_info(self):
        if not hasattr(self,'_parsed_package_info'):
            try:
                self._package_info = MultiValueDict(json.loads(self.package_info))
            except Exception, e:
                print str(e)
        return self._package_info
    
    @property
    def summary(self):
        return self.parsed_package_info.get('summary',u'')
    
    @property
    def description(self):
        return self.parsed_package_info.get('description',u'')
    
    def save(self, *args, **kwargs):
        if hasattr(self,'_package_info'):
            try:
                self.package_info = json.dumps(dict(self._package_info.iterlists()))
                delattr(self,'_package_info')
            except Exception, e:
                print str(e)
        return super(Release, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ('djangopypi-show_version', (), {'package': self.package.name,
                                                'version': self.version})


class File(models.Model):
    release = models.ForeignKey(Release, related_name="files")
    distribution = models.FileField(upload_to=settings.DJANGOPYPI_RELEASE_UPLOAD_TO)
    md5_digest = models.CharField(max_length=32, blank=True)
    filetype = models.CharField(max_length=32, blank=False,
                                choices=settings.DJANGOPYPI_DIST_FILE_TYPES)
    pyversion = models.CharField(max_length=16, blank=True,
                                 choices=settings.DJANGOPYPI_PYTHON_VERSIONS)
    comment = models.CharField(max_length=255, blank=True)
    signature = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    uploader = models.ForeignKey(User)
    
    @property
    def filename(self):
        return os.path.basename(self.distribution.name)
    
    @property
    def path(self):
        return self.distribution.name
    
    def get_absolute_url(self):
        return "%s#md5=%s" % (self.distribution.url, self.md5_digest)

    
    class Meta:
        verbose_name = _(u"file")
        verbose_name_plural = _(u"files")
        unique_together = ("release", "filetype", "pyversion")
    
    def __unicode__(self):
        return self.distribution.name

class Review(models.Model):
    release = models.ForeignKey(Release, related_name="reviews")
    rating = models.PositiveSmallIntegerField(blank=True)
    comment = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _(u'release review')
        verbose_name_plural = _(u'release reviews')
