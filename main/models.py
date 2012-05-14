from django.db import models
from django.db.models import Model, CharField, TextField, DateField, SlugField, URLField, ForeignKey

# Create your models here.

class Page(Model):
    #The page name/slug
    name = SlugField(max_length=32, unique=True)
    #The page title
    title = CharField(max_length=256)
    #Custom header content
    header_content = TextField(blank=True)
    
    #The actual content
    content = TextField()
    
    #display this in the admin interface
    def __unicode__(self):
        return self.name

class PageLink(Model):
    #Link name, used for templates/identifying by name
    name = SlugField(max_length=32, unique=True)
    #Title of the URL (the words that will be shown)
    title = CharField(max_length=256)
    #The actual location of the URL
    url = URLField(max_length=256)
    #The page that the link is related to
    page = ForeignKey('Page')
    
#class Resume(Model):
#    name = SlugField(max_length=64, unique=True)
#    title = CharField(max_length=256)

