from django import forms
from django.utils.translation import ugettext_lazy as _

from djangopypi.settings import settings
from djangopypi.models import Package, Classifier, Release



class SimplePackageSearchForm(forms.Form):
    query = forms.CharField(max_length=255)

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        exclude = ['name']

class ReleaseForm(forms.ModelForm):
    metadata_version = forms.CharField(widget=forms.Select(choices=zip(settings.DJANGOPYPI_METADATA_FIELDS.keys(),
                                                                       settings.DJANGOPYPI_METADATA_FIELDS.keys())))
    
    class Meta:
        model = Release
        exclude = ['package', 'version', 'package_info']

metadata10licenses = ('Artistic', 'BSD', 'DFSG', 'GNU GPL', 'GNU LGPL',
                     'MIT', 'Mozilla PL', 'public domain', 'Python',
                     'Qt', 'PL', 'Zope PL', 'unknown', 'nocommercial', 'nosell', 
                     'nosource', 'shareware', 'other')

class Metadata10Form(forms.Form):
    platform = forms.TextField(required=False,
                               help_text=_(u'A comma-separated list of platform '
                                           'specifications, summarizing the '
                                           'operating systems supported by the '
                                           'package.'))
    
    summary = forms.CharField(max_length=255,
                              help_text=_(u'A one-line summary of what the '
                                          'package does.'))
    
    description = forms.TextField(required=False,
                                  help_text=_(u'A longer description of the '
                                              'package that can run to several '
                                              'paragraphs. If this is in '
                                              'reStructuredText format, it will '
                                              'be rendered nicely on display.'))
    
    keywords = forms.CharField(max_length=255,
                               help_text=_(u'A list of additional keywords to '
                                           'be used to assist searching for the '
                                           'package in a larger catalog'))
    
    home_page = forms.URLField(max_length=255, required=False,
                               verify_exists=True,
                               help_text=_(u'A string containing the URL for '
                                           'the package\'s home page.'))
    
    author = forms.TextField(required=False,
                             help_text=_(u'A string containing at a minimum the '
                                         'author\'s name.  Contact information '
                                         'can also be added, separating each '
                                         'line with newlines.'))
    
    author_email = forms.CharField(max_length=255,
                                   help_text=_(u'A string containing the '
                                               'author\'s e-mail address.  It '
                                               'can contain a name and e-mail '
                                               'address in the legal forms for '
                                               'a RFC-822 \'From:\' header.'))
    
    license = forms.CharField(max_length=32,
                              help_text=_(u'A string selected from a short list '
                                          'of choices, specifying the license '
                                          'covering the package.'),
                              widget=forms.Select(choices=(zip(metadata10licenses,
                                                               metadata10licenses))))
    
class Metadata11Form(Metadata10Form):
    supported_platform = False
    download_url = False
    license = False
    classifier = False
    requires = False
    provides = False
    obsoletes = False

class Metadata12Form(Metadata10Form):
    supported_platform = False
    download_url = False
    license = False
    classifier = False
    maintainer = False
    maintainer_email = False
    requires_dist = False
    provides_dist = False
    obsoletes_dist = False
    requires_python = False
    requires_external = False
    project_url = False