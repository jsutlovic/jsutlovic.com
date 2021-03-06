from django.db import models
from django.db.models import (
    Model,
    SlugField,
    CharField,
    TextField,
    BooleanField,
    IntegerField,
    ForeignKey,
    OneToOneField,
    FileField,
    ManyToManyField,
    DateField,
    URLField,
    ImageField
)

#Options for date formatting
DATE_CHOICES = (('M Y', "Month and Year"), ('Y', "Year only"))
nums = tuple(range(100, -101, -1))
NUM_CHOICES = tuple(zip(nums, [str(n) for n in nums]))


#Find image path utility
def get_image_path(instance, filename):
    if isinstance(instance, ProjectImage):
        return "images/{project}/{filename}".format(
            {'project': instance.project.name, 'filename': filename})
    elif isinstance(instance, ProjectIcon):
        return "images/{project}/icon.png".format(
            {'project': instance.project.name})


def get_pdf_path(instance, filename):
    if isinstance(instance, Resume):
        return "files/resume/%(filename)s.pdf" % {'filename': instance.name}


class Page(Model):
    #The page name/slug
    name = SlugField(max_length=32, unique=True, help_text="The page name")
    #The page title
    title = CharField(max_length=256, help_text="The page title")
    #A description of the page
    description = CharField(
        max_length=256,
        help_text="A description of the page (used in meta fields)")

    #Custom header content
    header_content = TextField(blank=True, help_text="Custom header content")

    #The actual content
    content = TextField(help_text="The page content")

    #Whether the page will be full-height with content scrolling
    #or whether the page will expand with the content
    scrollable = BooleanField(
        default=False,
        help_text="full height with scroll or expand to fit")

    #display this in the admin interface
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('jsutlovic-page', [str(self.name)])


class Link(Model):
    """Common link fields"""

    #The link text
    name = CharField(max_length=128, help_text="Link text")

    #The words displayed
    title = CharField(max_length=128, help_text="Link title (hover text)")

    #The URL the site link refers to
    url = CharField(max_length=512, help_text="URL the link refers to")

    #Weight of the link (left to right order)
    weight = IntegerField(
        default=0,
        choices=NUM_CHOICES,
        help_text="Weight (display order)")

    #Disable the link?
    disabled = BooleanField(default=False, help_text="Disable link")

    class Meta:
        abstract = True
        ordering = ['-weight', 'name']


class PageLink(Link):
    #The page that the link is related to
    page = ForeignKey('Page', related_name="links", help_text="Related page")

    #Display this in the admin interface
    def __unicode__(self):
        return ' - '.join([self.page.title, self.name])


class SiteLink(Link):
    #Is it a Primary link? (top of page)
    primaryLinks = BooleanField(
        default=False,
        help_text="Primary link (top of page)")

    #Secondary link? (bottom of page)
    secondaryLinks = BooleanField(
        default=False,
        help_text="Secondary link (bottom of page)")

    #Related pages
    page = OneToOneField(
        'Page',
        null=True,
        blank=True,
        help_text="Related page")

    def __unicode__(self):
        return self.name


class ContactDetail(Model):
    #The type of the contact detail (website, email, etc)
    type = CharField(max_length=64, help_text="Type, e.g. website, email, url")

    #The value (text displayed)
    value = CharField(max_length=256, help_text="Text displayed")

    #If it's a link, the URL to go to
    url = CharField(max_length=512, blank=True, help_text="Associated URL")

    #The weight (vertical position)
    weight = IntegerField(
        default=0,
        choices=NUM_CHOICES,
        help_text="Weight (order displayed)")

    #For schema.org microdata markup
    itemprop = CharField(
        max_length=32,
        blank=True,
        help_text="For schema.org microdata")

    class Meta:
        ordering = ["-weight"]

    def __unicode__(self):
        return " - ".join((self.type, self.value))


#Resume

class Resume(Model):
    #resume name, unique. Used for ID (HTML)
    name = SlugField(
        max_length=32,
        unique=True,
        help_text="Unique name of resume")

    #What it's called
    title = CharField(
        max_length=64,
        help_text="Resume Title")

    #Which order the resume is displayed.
    #Resume with highest weight is shown on /resume page
    weight = IntegerField(
        default=0,
        choices=NUM_CHOICES,
        help_text="Resume with highest weight is displayed on /resume")

    #HTML for resume's contact info section
    contactInfo = TextField(
        blank=True,
        help_text="Contact information (displayed in header, HTML allowed)")

    #HTML for resume's footer section
    footer = TextField(
        blank=True,
        help_text="Resume footer (HTML allowed)")

    #PDF file for resume
    pdf = FileField(
        upload_to=get_pdf_path,
        blank=True,
        help_text="PDF version")

    #Resume data in YAML format
    data = TextField(help_text="YAML resume data")

    #sections = ManyToManyField - ResumeSection

    class Meta:
        ordering = ['-weight']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('jsutlovic-resume-name', [str(self.name)])


class Project(Model):
    #Project shortname
    name = SlugField(
        max_length=32,
        unique=True,
        help_text="Shortname for the project")

    #Title (displayed name) of project
    title = CharField(
        max_length=64,
        help_text="Title (displayed name) of project")

    #Description of the project
    description = TextField(help_text="Project description")

    #URL of the project, if any
    url = URLField(blank=True, help_text="URL to project")

    #How the dates should be displayed (if at all)
    dateDisplay = CharField(
        max_length=16,
        blank=True,
        choices=DATE_CHOICES,
        help_text="Date formatting: Year/month and year/etc.")

    #Date of start (if any)
    dateFrom = DateField(
        null=True,
        blank=True,
        help_text="Date project started")

    #Date of end (else consider current)
    dateTo = DateField(
        null=True,
        blank=True,
        help_text="Date project completed")

    #The weight of the project
    weight = IntegerField(default=0, choices=NUM_CHOICES, help_text="Ordering")

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
    name = SlugField(max_length=32, unique=True, help_text="Tag name")

    #Related project
    projects = ManyToManyField(
        'Project',
        related_name='tags',
        help_text="Related projects")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('jsutlovic-projects-techtag', [str(self.name)])


class ProjectImage(Model):
    #A short image description
    title = CharField(max_length=128, help_text="Image description")

    #Related project
    project = ForeignKey(
        'Project',
        related_name='images',
        help_text="Related project")

    #The image file
    image = ImageField(upload_to=get_image_path, help_text="Image file")

    #For display ordering
    weight = IntegerField(default=0, choices=NUM_CHOICES, help_text="Ordering")

    class Meta:
        ordering = ['-weight']

    def __unicode__(self):
        return self.title


class ProjectIcon(Model):
    #Related project this thumbnail is for
    project = OneToOneField(
        'Project',
        related_name='icon',
        help_text="Related project")

    #The image file
    image = ImageField(upload_to=get_image_path, help_text="Image file")

    def __unicode__(self):
        return "%s %s" % (self.project.name, "icon")
