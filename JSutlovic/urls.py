from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from main.sitemaps import sitemaps

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

if settings.UNDER_CONSTRUCTION:
    index = 'under_construction'
else:
    index = 'about'

urlpatterns = patterns('main.views',
    url(r'^$', index, name='jsutlovic-index'),
    url(r'^about$', 'about', name='jsutlovic-about'),
    url(r'^contact$', 'contact', name='jsutlovic-contact'),
    url(r'^resume$', 'resume', name='jsutlovic-resume'),
    url(r'^resume/plain$', 'resume', {"plain": True}, name='jsutlovic-resume-plain'),
    url(r'resume/(?P<name>\S+)/plain$', 'resume', {"plain": True}, name='jsutlovic-resume-name-plain'),
    url(r'^resume/(?P<name>\S+)$', 'resume', name='jsutlovic-resume-name'),
    url(r'^work$', 'projects', name='jsutlovic-projects'),
    url(r'^work/tech/(?P<techtag>\S+)$', 'projects', {"name":None}, name='jsutlovic-projects-techtag'),
    #url(r'^work/(?P<name>\S+)$', 'projects', name='jsutlovic-projects-name'),
    url(r'^bcard$', RedirectView.as_view(url='/contact', permanent=False)),
)

if settings.DEVELOPMENT:
    urlpatterns += patterns(
        '',
        #Static files (development)
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS[0]}),
        #Media serving (development)
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

#Admin pages
if settings.ADMIN_ENABLED:
    urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)),)

#Extras
urlpatterns += patterns('',
    #Robots.txt
    url(r'^robots\.txt$', 'main.views.robots', name='jsutlovic-robots'),
    
    #Favicon
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon16.ico')),

    #Sitemap
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    #Page catch-all
    url(r'^(?P<name>\S+)$', 'main.views.page', name='jsutlovic-page'),
)

handler404 = "main.views.handler404"
handler500 = "main.views.handler500"