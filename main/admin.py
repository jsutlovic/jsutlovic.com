from main.models import (
    Page,
    PageLink,
    SiteLink,
    ContactDetail,
    Resume,
    Project,
    ProjectTechTag,
    ProjectIcon,
    ProjectImage
)
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
    list_display = ('name', 'title', 'url', 'weight',
                    'primaryLinks', 'secondaryLinks', 'disabled')
    list_display_links = ('name', 'title', 'url', 'weight')
    ordering = ('-primaryLinks', '-weight', 'name')

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

    def has_add_permission(self, request):
        return True


class ProjectImageInline(TabularInline):
    model = ProjectImage
    extra = 1


class ProjectAdmin(ModelAdmin):
    list_display = ('name', 'title', 'weight')
    list_display_links = ('name', 'title', 'weight')
    ordering = ('-weight', '-dateTo')
    inlines = (ProjectIconInline, ProjectTechTagInline, ProjectImageInline)

admin.site.register(Project, ProjectAdmin)


class ProjectTechTagAdmin(ModelAdmin):
    list_display = ('name',)

admin.site.register(ProjectTechTag, ProjectTechTagAdmin)
