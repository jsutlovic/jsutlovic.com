from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'JSutlovic.views.home', name='home'),
    # url(r'^JSutlovic/', include('JSutlovic.foo.urls')),
    
    url(r'^$', 'main.views.about', name='jsutlovic-index'),
    url(r'^about$', 'main.views.about', name='jsutlovic-about'),
    url(r'^contact$', 'main.views.contact', name='jsutlovic-contact'),
    url(r'^resume$', 'main.views.resume', name='jsutlovic-resume'),
    url(r'^resume/(?P<name>\S+)$', 'main.views.resume', name='jsutlovic-resume-name'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #Page catch-all
    url(r'^(?P<name>\S+)$', 'main.views.page', name='jsutlovic-page'),
)

urlpatterns += staticfiles_urlpatterns()
