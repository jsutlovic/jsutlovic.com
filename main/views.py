# Create your views here.

from django.shortcuts             import render_to_response, get_object_or_404, redirect
from django.template              import Context, loader, RequestContext
from django.http                  import HttpResponse, Http404

from ocds.ocds_main.models import *


def rr(template, context, request):
    return render_to_response(template, context, context_instance=RequestContext(request))

def about(request):
    page = "about"

    r = get_object_or_404( Page, name=page )
    return rr("page.html", {"page": r}, request)
