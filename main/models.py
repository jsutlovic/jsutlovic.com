from django.db import models
from django.db.models import *

#Options for date formatting
DATE_CHOICES = (('M Y', "Month and Year"), ('Y', "Year only"))
nums = tuple(range(100, -101, -1))
NUM_CHOICES = tuple(zip(nums, [str(n) for n in nums]))

#Find image path utility
def get_image_path(instance, filename):
    if isinstance(instance, ProjectImage):
        return "images/%(project)s/%(filename)s" % {'project': instance.project.name, 'filename': filename}
    elif isinstance(instance, ProjectIcon):
        return "images/%(project)s/icon.png" % {'project': instance.project.name}

class Page(Model):
    #The page name/slug
    name = SlugField(max_length=32, unique=True, help_text="The page name")
    #The page title
    title = CharField(max_length=256, help_text="The page title")
    #A description of the page
    description = CharField(max_length=256, help_text="A description of the page (used in meta fields)")
    
    #Custom header content
    header_content = TextField(blank=True, help_text="Custom header content")
    
    #The actual content
    content = TextField(help_text="The page content")
    
    #Whether the page will be full-height with content scrolling or expand the page
    scrollable = BooleanField(default=False, help_text="full height with scroll or expand to fit")
    
    #display this in the admin interface
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('jsutlovic-page', [str(self.name)])
        

class Link(Model):
    """Common link fields"""
    
    #The link text
    name = CharField(max_length=128, help_text="Link name")
    
    #The words displayed
    title = CharField(max_length=128, help_text="Words displayed")
    
    #The URL the site link refers to
    url = CharField(max_length=512, help_text="URL the link refers to")
    
    #Weight of the link (left to right order)
    weight = IntegerField(default=0, choices=NUM_CHOICES, help_text="Weight (display order)")

    #Disable the link?
    disabled = BooleanField(default=False, help_text="Disable link")
    
    class Meta:
        abstract=True
        ordering=['-weight', 'name']
    

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
    weight = IntegerField(default=0, choices=NUM_CHOICES)
    
    #For schema.org microdata markup
    itemprop = CharField(max_length=32, blank=True)
    
    class Meta:
        ordering = ["-weight"]
    
    def __unicode__(self):
        return " - ".join((str(self.weight), self.type, self.value))
    

#Resume > Section > Subsection > Detail

class Resume(Model):
    #resume name, unique. Used for ID (HTML)
    name = SlugField(max_length=32, unique=True)
    
    #What it's called
    title = CharField(max_length=64)
    
    #Which order the resume is displayed.
    #Resume with highest weight is shown on /resume page
    weight = IntegerField(default=0, choices=NUM_CHOICES)
    
    #HTML for resume's contact info section
    contactInfo = TextField(blank=True)
    
    #HTML for resume's footer section
    footer = TextField(blank=True)
    
    pdf = BooleanField(default=False)
    
    #sections = ManyToManyField - ResumeSection
    
    class Meta:
        ordering = ['-weight']
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('jsutlovic-resume-name', [str(self.name)])
    
class ResumeSection(Model):
    #Unique name of the section (used for HTML)
    name = SlugField(max_length=64, unique=True)
    
    #Title of the section
    title = CharField(max_length=64)
    
    #Weight of the section (where it's displayed)
    weight = IntegerField(default=0, choices=NUM_CHOICES)
    
    #The resume the section is associated with
    resume = ManyToManyField('Resume', related_name='sections')
    
    #subsections = ForeignKey - ResumeSubSection
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['-weight']
        

class ResumeSubSection(Model):
    #Subsection name (used for HTML)
    name = CharField(max_length=64)
    
    #Title of the subsection
    title = CharField(max_length=128)
    
    #Weight of the section (where it's displayed)
    weight = IntegerField(default=0, choices=NUM_CHOICES)
    
    #How do we display dates? (Options to pass to Django's built in date filter
    dateDisplay = CharField(max_length=16, blank=True, choices=DATE_CHOICES)
    
    #Date of start (if any)
    dateFrom = DateField(null=True, blank=True)
    
    #Date of end (if any)
    dateTo = DateField(null=True, blank=True)
    
    #The section it's related to
    section = ForeignKey('ResumeSection', related_name='subsections')
    
    #details = ForeignKey - ResumeDetail
    
    def __unicode__(self):
        return self.title
    
    #Default order is by descending weight
    class Meta:
        ordering = ['-weight']
    
    
class ResumeDetail(Model):
    #Weight of the detail
    weight = IntegerField(default=0, choices=NUM_CHOICES)
    
    #Detail contents
    contents = CharField(max_length=256)
    
    #Related subsection
    subsection = ForeignKey('ResumeSubSection', related_name='details')
    
    #Show as subsection - contents
    def __unicode__(self):
        return " - ".join([self.subsection.name, self.contents])
    
    #Order by descending weight
    class Meta:
        ordering = ['-weight']


class Project(Model):
    #Project shortname
    name = SlugField(max_length=32, unique=True)
    
    #Title (displayed name) of project
    title = CharField(max_length=64)
    
    #Description of the project
    description = TextField()
    
    #URL of the project, if any
    url = URLField(blank=True)
    
    #How the dates should be displayed (if at all)
    dateDisplay = CharField(max_length=16, blank=True, choices=DATE_CHOICES)
    
    #Date of start (if any)
    dateFrom = DateField(null=True, blank=True)
    
    #Date of end (else consider current)
    dateTo = DateField(null=True, blank=True)
    
    #The weight of the project
    weight = IntegerField(default=0, choices=NUM_CHOICES)
    
    #tags = ManyToMany - ProjectTechTag
    #images = ForeignKey - ProjectImage
    #icon = ProjectIcon
    
    def __unicode__(self):
        return self.title 
    
    def get_tags(self):
        return self.tags.all().order_by('name')
    
    def get_images(self):
        return self.images.all().order_by('-weight')


class ProjectTechTag(Model):
    #Name of the tag
    name = SlugField(max_length=32, unique=True)
    
    #Related project
    projects = ManyToManyField('Project', related_name='tags')
    
    def __unicode__(self):
        return self.name
    
class ProjectImage(Model):
    #A short image description
    title = CharField(max_length=128)
    
    #Related project
    project = ForeignKey('Project', related_name='images')
    
    #The image file
    image = ImageField(upload_to=get_image_path)
    
    #For display ordering
    weight = IntegerField(default=0, choices=NUM_CHOICES)
    
    class Meta:
        ordering = ['-weight']
        
    def __unicode__(self):
        return self.title
    
    
class ProjectIcon(Model):
    #Related project this thumbnail is for
    project = OneToOneField('Project', related_name='icon')
    
    #The image file
    image = ImageField(upload_to=get_image_path)
    
    def __unicode__(self):
        return "%s %s" % (self.project.name, "icon")






