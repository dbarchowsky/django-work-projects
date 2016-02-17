from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.core import urlresolvers
from django.db import models
from django.forms import Textarea
from django.core.urlresolvers import ViewDoesNotExist, Resolver404, NoReverseMatch
from work_projects.models import Project, ProjectType, ProjectSample, Gallery, Asset, Tag


class AssetInline(GenericTabularInline):
    model = Asset
    extra = 0
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(
                attrs={
                    'style': 'height: 12em;',
                }
            )
        }
    }
    sortable_field_name = 'slot'


class GalleryInline(GenericTabularInline):
    model = Gallery
    extra = 0
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(
                attrs={
                    'style': 'height: 6em;',
                }
            )
        }
    }


class AssetTagInline(admin.TabularInline):
    model = Asset.tags.through
    verbose_name = "Tag"
    verbose_name_plural = "Tags"
    extra = 1


class GalleryTagInline(admin.TabularInline):
    model = Gallery.tags.through
    verbose_name = "Tag"
    verbose_name_plural = "Tags"
    extra = 1


class ProjectSampleAdmin(admin.ModelAdmin):
    list_display = ['name', 'project_full_path', 'asset_count', 'gallery_count', 'enabled', ]
    inlines = [
        AssetInline,
        GalleryInline,
    ]
    exclude = ['tags', ]

admin.site.register(ProjectSample, ProjectSampleAdmin)


class ProjectSampleInline(admin.StackedInline):
    model = ProjectSample
    extra = 1
    readonly_fields = ('changeform_link', )
    sortable_field_name = 'slot'

    def changeform_link(self, instance):
        self.is_not_used()
        try:
            if instance.id:
                # URL pattern is app_name+underscore+model_name+underscore+"change":
                changeform_url = urlresolvers.reverse(
                    'admin:work_projects_projectsample_change', args=(instance.id,)
                )
                return u'<a href="%s" target="_blank">Details</a>' % changeform_url
            return u''
        except ViewDoesNotExist:
            return u'error: View does not exist.'
        except Resolver404:
            return u'URL resolver error: Resolver 404.'
        except NoReverseMatch:
            return u'URL resolver error: No reverse match.'
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header

    def is_not_used(self):
        pass


class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'project_count', 'enabled', 'is_default', ]
    prepopulated_fields = {'slug': ('name', )}

    def project_count(self, instance):
        self.is_not_used()
        return "%d" % instance.projects.count()
    project_count.short_description = "Projects"

    def is_not_used(self):
        pass


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', ]
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Tag, TagAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'type_name', 'sample_count', 'enabled', ]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        ProjectSampleInline,
    ]
    sortable_field_name = 'slot'

    def is_not_used(self):
        pass

admin.site.register(ProjectType, ProjectTypeAdmin)
admin.site.register(Project, ProjectAdmin)


class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_name', 'parent_type', 'image', 'caption', 'tag_names', ]
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }
    inlines = [ AssetTagInline, ]
    exclude = ['tags', ]

admin.site.register(Asset, AssetAdmin)


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_name', 'parent_type', 'asset_count', 'slug', 'tag_names', ]
    prepopulated_fields = {"slug": ('name', )}
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }
    inlines = [
        AssetInline,
        GalleryTagInline,
    ]
    exclude = ['tags', ]

admin.site.register(Gallery, GalleryAdmin)
