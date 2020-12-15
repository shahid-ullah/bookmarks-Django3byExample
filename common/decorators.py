# common/decorators.py

from django.http import HttpResponse, HttpResponseBadRequest


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        """TODO: Docstring for wrap.

        :arg1: TODO
        :returns: TODO

        """
        if not request.is_ajax():
            return HttpResponseBadRequest()
            return HttpResponse('Stillness is the of everything')
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
