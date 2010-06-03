try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps

from django.conf import settings
from django.contrib.auth import login
from django.utils.decorators import available_attrs

from djangopypi.http import HttpResponseUnauthorized, login_basic_auth



def basic_auth(view_func):
    """
    Decorator for views that need to handle basic authentication such as 
    distutils views.
    """
    
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        user = login_basic_auth(request)
        
        if not user:
            return HttpResponseUnauthorized('pypi')
        
        login(request, user)
        if not request.user.is_authenticated():
            return HttpResponseForbidden("Not logged in, or invalid username/"
                                         "password.")
        return view_func(request, *args, **kwargs)
    return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
