import os
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

OS_NAMES = (
        ("aix", "AIX"),
        ("beos", "BeOS"),
        ("debian", "Debian Linux"),
        ("dos", "DOS"),
        ("freebsd", "FreeBSD"),
        ("hpux", "HP/UX"),
        ("mac", "Mac System x."),
        ("macos", "MacOS X"),
        ("mandrake", "Mandrake Linux"),
        ("netbsd", "NetBSD"),
        ("openbsd", "OpenBSD"),
        ("qnx", "QNX"),
        ("redhat", "RedHat Linux"),
        ("solaris", "SUN Solaris"),
        ("suse", "SuSE Linux"),
        ("yellowdog", "Yellow Dog Linux"),
)

ARCHITECTURES = (
    ("alpha", "Alpha"),
    ("hppa", "HPPA"),
    ("ix86", "Intel"),
    ("powerpc", "PowerPC"),
    ("sparc", "Sparc"),
    ("ultrasparc", "UltraSparc"),
)

DIST_FILE_TYPES = (
    ('sdist','Source'),
    ('bdist_dumb','"dumb" binary'),
    ('bdist_rpm','RPM'),
    ('bdist_wininst','MS Windows installer'),
    ('bdist_egg','Python Egg'),
    ('bdist_dmg','OS X Disk Image'),
)

PYTHON_VERSIONS = (
    ('any','Any i.e. pure python'),
    ('2.1','2.1'),
    ('2.2','2.2'),
    ('2.3','2.3'),
    ('2.4','2.4'),
    ('2.5','2.5'),
    ('2.6','2.6'),
    ('2.7','2.7'),
    ('3.0','3.0'),
    ('3.1','3.1'),
    ('3.2','3.2'),
)

UPLOAD_TO = getattr(settings,
    "DJANGOPYPI_RELEASE_UPLOAD_TO", 'dist')

class Classifier(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _(u"classifier")
        verbose_name_plural = _(u"classifiers")

    def __unicode__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    auto_hide = models.BooleanField(default=True, blank=False)
    allow_comments = models.BooleanField(default=True, blank=False)
    owners = models.ManyToManyField(User, related_name="projects_owned")
    maintainers = models.ManyToManyField(User, related_name="projects_maintained")
    
    class Meta:
        verbose_name = _(u"project")
        verbose_name_plural = _(u"projects")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('djangopypi-show_links', (), {'dist_name': self.name})

    @models.permalink
    def get_pypi_absolute_url(self):
        return ('djangopypi-pypi_show_links', (), {'dist_name': self.name})

    def get_release(self, version):
        """Return the release object for version, or None"""
        try:
            return self.releases.get(version=version)
        except Release.DoesNotExist:
            return None

class Release(models.Model):
    project = models.ForeignKey(Project, related_name="releases")
    version = models.CharField(max_length=128)
    metadata_version = models.CharField(max_length=64, default='1.0')
    package_info = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        verbose_name = _(u"release")
        verbose_name_plural = _(u"releases")
        unique_together = ("project", "version")

    def __unicode__(self):
        return self.release_name
    
    @property
    def release_name(self):
        return u"%s-%s" % (self.project.name, self.version)
    
    @models.permalink
    def get_absolute_url(self):
        return ('djangopypi-show_version', (), {'project': self.project.name,
                                                'version': self.version})


class File(models.Model):
    release = models.ForeignKey(Release, related_name="files")
    distribution = models.FileField(upload_to=UPLOAD_TO)
    md5_digest = models.CharField(max_length=32, blank=True)
    filetype = models.CharField(max_length=255, blank=False,
                                choices=DIST_FILE_TYPES)
    pyversion = models.CharField(max_length=255, blank=True,
                                 choices=PYTHON_VERSIONS)
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
