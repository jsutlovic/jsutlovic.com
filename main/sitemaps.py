from datetime import date
from django.contrib.sitemaps import Sitemap
from main.models import Page, Resume, ProjectTechTag

LASTMOD = date(2012, 6, 4)

class PageSitemap(Sitemap):
    changefreq="monthly"
    priority=0.9
    
    def items(self):
        return Page.objects.all()
    
    def lastmod(self, page):
        return LASTMOD

class ResumeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    
    def items(self):
        return Resume.objects.all()
    
    def lastmod(self, resume):
        return LASTMOD

class ResumePlainSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    
    def items(self):
        return Resume.objects.all()
        
    def lastmod(self, resume):
        return LASTMOD
    
    def location(self, resume):
        return resume.get_absolute_url()+"/plain"

class ProjectTechtagSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.4
    
    def items(self):
        return ProjectTechTag.objects.all()
        
    def lastmod(self, tag):
        return LASTMOD

sitemaps = {
    'pages': PageSitemap,
    'resumes': ResumeSitemap,
    'plainresumes': ResumePlainSitemap,
    'projecttags': ProjectTechtagSitemap,
}
    