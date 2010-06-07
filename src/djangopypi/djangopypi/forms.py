import os
from django import forms
from django.conf import settings
from djangopypi.models import Package, Classifier, Release
from django.utils.translation import ugettext_lazy as _

class SimplePackageSearchForm(forms.Form):
    query = forms.CharField(max_length=255)

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        exclude = ['name']


class ReleaseForm(forms.ModelForm):
    class Meta:
        model = Release
        exclude = ['package']