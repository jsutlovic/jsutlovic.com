# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import loader, RequestContext
from django.http import HttpResponseNotFound, HttpResponseServerError

import logging

from main.models import Page, SiteLink, ContactDetail, Resume, \
    Project, ProjectTechTag


logger = logging.getLogger(__name__)


def rr(template, context, request, status=200):
    links = {"primary":
             SiteLink.objects.filter(
                 primaryLinks=True,
                 disabled=False
             ).order_by('-weight'),
             "secondary":
             SiteLink.objects.filter(
                 secondaryLinks=True,
                 disabled=False
             ).order_by('-weight'),
             }

    if "page" in context and isinstance(context["page"], Page):
        links["page"] = context["page"].linksq.filter(disabled=False) \
                                       .order_by('-weight')

    context["links"] = links

    if status == 404:
        return HttpResponseNotFound(
            loader.render_to_string(template, context,
                                    RequestContext(request)))
    elif status == 500:
        return HttpResponseServerError(
            loader.render_to_string(template, context,
                                    RequestContext(request)))

    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def about(request):
    rpage = get_object_or_404(Page, name="about")
    return rr("page.djhtml", {"page": rpage}, request)


def contact(request):
    rpage = get_object_or_404(Page, name="contact")

    details = ContactDetail.objects.all().order_by('-weight')

    return rr("contact.djhtml", {"page": rpage, "details": details}, request)


def resume(request, name="", plain=False):
    rpage = get_object_or_404(Page, name="resume")

    if not name:
        rres = Resume.objects.all().order_by('-weight')[0]
    else:
        rres = get_object_or_404(Resume, name=name)

    if plain:
        return rr("resume-plain.djhtml",
                  {"page": rpage, "resume": rres},
                  request)

    return rr("resume-inpage.djhtml", {"page": rpage, "resume": rres}, request)


def projects(request, name="", techtag=""):
    rpage = get_object_or_404(Page, name='work')
    if not (name or techtag):
        rprojects = Project.objects.all().order_by('-weight')
        return rr("projects.djhtml",
                  {"page": rpage, "projects": rprojects}, request)
    elif techtag:
        ptt = get_object_or_404(ProjectTechTag, name=techtag)
        rprojects = ptt.projects.all().order_by('-weight')
        return rr("projects.djhtml",
                  {"page": rpage, "projects": rprojects}, request)
    elif name:
        rproject = get_object_or_404(Project, name=name)
        return rr("project.djhtml",
                  {"page": rpage, "project": rproject}, request)


def page(request, name=""):
    if not name:
        return about(request)

    #Redirect about page
    if name == "about":
        return redirect("jsutlovic-index")

    rpage = get_object_or_404(Page, name=name)

    return rr("page.djhtml", {"page": rpage}, request)


def under_construction(request):
    epage = {'name': "under_construction",
             'title': "Under Construction",
             'description': "JSutlovic.com is under construction",
             'header_content': "",
             'content': (
                 "<p>JSutlovic.com is under construction but don't worry, "
                 "the real site will be up in no time.</p>"),
             'scrollable': True}

    return render_to_response("page.djhtml", {"page": epage},
                              context_instance=RequestContext(request))


def robots(request):
    return render_to_response("robots.txt", mimetype="text/plain")


def handler404(request):
    epage = {'name': "404",
             'title': "Page Not Found",
             'description': "Page not found",
             'header_content': "",
             'content': (
                 "<p>Looks like the page you're looking for isn't here.</p>"),
             'scrollable': True}

    return rr("page.djhtml", {"page": epage}, request, status=404)


def handler500(request):
    epage = {'name': "500",
             'title': "Server Error",
             'description': "Server Error",
             'header_content': "",
             'content': "<p>Uhoh, looks like the server made a boo-boo.</p>",
             'scrollable': True}

    return rr("page.djhtml", {"page": epage}, request, status=500)
