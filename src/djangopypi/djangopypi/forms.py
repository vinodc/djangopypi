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

