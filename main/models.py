from django.db import models
from django.db.models import Model, CharField, TextField, DateField, SlugField, URLField, ForeignKey, BooleanField, IntegerField, OneToOneField

# Create your models here.

class Page(Model):
    #The page name/slug
    name = SlugField(max_length=32, unique=True)
    #The page title
    title = CharField(max_length=256)
    #A description of the page
    description = CharField(max_length=256)
    
    #Custom header content
    header_content = TextField(blank=True)
    
    #The actual content
    content = TextField()
    
    #Whether the page will be full-height with content scrolling or expand the page
    scrollable = BooleanField(default=False)
    
    #display this in the admin interface
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('jsutlovic-page', [str(self.name)])
        

class Link(Model):
    """Common link fields"""
    
    #The link text
    name = CharField(max_length=128)
    
    #The words displayed
    title = CharField(max_length=128)
    
    #The URL the site link refers to
    url = CharField(max_length=512)
    
    #Weight of the link (left to right order)
    weight = IntegerField(default=0)

    #Disable the link?
    disabled = BooleanField(default=False)
    
    class Meta:
        abstract=True
        ordering=['name', '-weight']
    

class PageLink(Link):
    #The page that the link is related to
    page = ForeignKey('Page', related_name="links")
    
    #Display this in the admin interface
    def __unicode__(self):
        return ' - '.join([self.page.title, self.name])


class SiteLink(Link):
    #Is it a Primary link? (top of page)
    primaryLinks = BooleanField(default=False)
    
    #Secondary link? (bottom of page)
    secondaryLinks = BooleanField(default=False)
    
    #Related pages
    page = OneToOneField('Page', null=True, blank=True)
    
    def __unicode__(self):
        return self.name


class ContactDetail(Model):
    #The type of the contact detail (website, email, etc)
    type = CharField(max_length=64)
    
    #The value (text displayed)
    value = CharField(max_length=256)
    
    #If it's a link, the URL to go to
    url = URLField(max_length=512, blank=True)
    
    #The weight (vertical position)
    weight = IntegerField(default=0)
    
    def __unicode__(self):
        return self.value


