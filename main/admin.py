from main.models import *
from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline

class PageAdmin(ModelAdmin):
    list_display = ('name', 'title')
    ordering = ('name',)

admin.site.register(Page, PageAdmin)

class PageLinkAdmin(ModelAdmin):
    list_display = ('name', 'title', 'url', 'weight', 'disabled')
    list_display_links = ('name', 'title', 'url', 'weight')
    ordering = ('-weight', 'name')

admin.site.register(PageLink, PageLinkAdmin)

class SiteLinkAdmin(ModelAdmin):
    list_display = ('name', 'title', 'url', 'weight', 'primaryLinks', 'secondaryLinks', 'disabled')
    list_display_links = ('name', 'title', 'url', 'weight')
    ordering= ('-weight', 'name')

admin.site.register(SiteLink, SiteLinkAdmin)

class ContactDetailAdmin(ModelAdmin):
    list_display = ('type', 'value', 'url', 'weight')
    list_display_links = ('type', 'value', 'url', 'weight')
    ordering = ('-weight', 'type', )

admin.site.register(ContactDetail, ContactDetailAdmin)


#Resume admins
class ResumeAdmin(ModelAdmin):
    list_display = ('name', 'title', 'weight', 'pdf')
    list_display_links = ('name', 'title', 'weight')
    
admin.site.register(Resume, ResumeAdmin)

class ResumeSectionAdmin(ModelAdmin):
    list_display = ('name', 'title', 'weight')
    list_display_links = ('name', 'title', 'weight')
    
admin.site.register(ResumeSection, ResumeSectionAdmin)

class ResumeSubSectionAdmin(ModelAdmin):
    list_display = ('name', 'title', 'weight', 'section')
    list_display_links = ('name', 'title', 'weight')
    ordering = ('section', '-weight', )

admin.site.register(ResumeSubSection, ResumeSubSectionAdmin)

class ResumeDetailAdmin(ModelAdmin):
    list_display = ('contents', 'weight', 'subsection')
    list_display_links = ('contents', 'weight')
    ordering = ('subsection', '-weight', )

admin.site.register(ResumeDetail, ResumeDetailAdmin)


#Project admins

class ProjectIconInline(StackedInline):
    model = ProjectIcon
    extra = 1
    
    #Don't allow deleting icons
    def has_delete_permission(self, request, obj=None):
        return False

class ProjectTechTagInline(TabularInline):
    model = ProjectTechTag.projects.through
    extra = 1

class ProjectImageInline(TabularInline):
    model = ProjectImage
    extra = 1

class ProjectAdmin(ModelAdmin):
    list_display = ('name', 'title', 'weight')
    list_display_links = ('name', 'title', 'weight')
    ordering = ('-weight',)
    inlines = (ProjectIconInline, ProjectTechTagInline, ProjectImageInline)

admin.site.register(Project, ProjectAdmin)
