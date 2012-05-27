from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('main.views',
    # Examples:
    # url(r'^$', 'JSutlovic.views.home', name='home'),
    # url(r'^JSutlovic/', include('JSutlovic.foo.urls')),
    
    url(r'^$', 'about', name='jsutlovic-index'),
    url(r'^about$', 'about', name='jsutlovic-about'),
    url(r'^contact$', 'contact', name='jsutlovic-contact'),
    url(r'^resume$', 'resume', name='jsutlovic-resume'),
    url(r'^resume/plain$', 'resume', {"plain": True}, name='jsutlovic-resume-plain'),
    url(r'resume/(?P<name>\S+)/plain$', 'resume', {"plain": True}, name='jsutlovic-resume-name-plain'),
    url(r'^resume/(?P<name>\S+)$', 'resume', name='jsutlovic-resume-name'),
    url(r'^work$', 'projects', name='jsutlovic-projects'),
    url(r'^work/(?P<name>\S+)$', 'projects', name='jsutlovic-projects-name'),
    url(r'^work/tech/(?P<techtag>\S+)$', 'projects', name='jsutlovic-projects-techtag'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
)

#Static files (development)
urlpatterns += staticfiles_urlpatterns()

#Media serving (development)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Extras
urlpatterns += patterns('',
                        # Uncomment the next line to enable the admin:
                        url(r'^admin/', include(admin.site.urls)),
                        
                        #Page catch-all
                        url(r'^(?P<name>\S+)$', 'main.views.page', name='jsutlovic-page'),
)