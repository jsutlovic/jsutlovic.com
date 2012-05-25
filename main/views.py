# Create your views here.

from django.shortcuts             import render_to_response, get_object_or_404, redirect
from django.template              import Context, loader, RequestContext
from django.http                  import HttpResponse, Http404

from main.models import Page, SiteLink, ContactDetail, Resume


def rr(template, context, request):
    links = {"primary": SiteLink.objects.filter(primaryLinks=True, disabled=False).order_by('-weight'),
             "secondary": SiteLink.objects.filter(secondaryLinks=True, disabled=False).order_by('-weight'),
            }
    
    if "page" in context and isinstance(context["page"], Page):
        links["page"] = context["page"].links.filter(disabled=False).order_by('-weight')
    
    context["links"] = links
    
    return render_to_response(template, context, context_instance=RequestContext(request))

def about(request):
    rpage = get_object_or_404( Page, name="about" )
    
    return rr("page.djhtml", {"page": rpage}, request)


def contact(request):
    rpage = get_object_or_404( Page, name="contact" )
    
    details = ContactDetail.objects.all().order_by('-weight')
    
    return rr("contact.djhtml", {"page": rpage, "details": details}, request)


def resume(request, name=""):
    rpage = get_object_or_404( Page, name="resume" )
    
    if not name:
        rres = Resume.objects.all().order_by('-weight')[0]
    else:
        rres = get_object_or_404( Resume, name=name )
    
    return rr("resume-inpage.djhtml", {"page": rpage, "resume": rres}, request)
    

def page(request, name=""):
    if not name:
        return about(request)
    
    #Redirect about page
    if name == "about":
        return redirect("jsutlovic-index")
    
    rpage = get_object_or_404( Page, name=name )
    
    return rr("page.djhtml", {"page": rpage}, request)

