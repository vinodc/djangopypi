from djangopypi.models import Package, Release

try:
    from django.contrib.syndication.views import Feed, FeedDoesNotExist
except ImportError:
    from django.contrib.syndication.feeds import Feed as BaseFeed, FeedDoesNotExist
    from django.http import HttpResponse, Http404
    from django.core.exceptions import ObjectDoesNotExist
    
    class Feed(BaseFeed):
        def __call__(self, request, *args, **kwargs):
            try:
                obj = self.get_object(request, *args, **kwargs)
            except ObjectDoesNotExist:
                raise Http404('Feed object does not exist.')
            feedgen = self.get_feed(obj, request)
            response = HttpResponse(mimetype=feedgen.mime_type)
            feedgen.write(response, 'utf-8')
            return response

class ReleaseFeed(Feed):
    """ A feed of releases either for the site in general or for a specific 
    package. """
    pass


