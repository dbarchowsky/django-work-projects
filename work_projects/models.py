from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class ProjectType(models.Model):
    name = models.CharField(default="", max_length=50)
    slug = models.SlugField(default="")
    enabled = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, default="")
    client = models.ForeignKey('work_clients.Client')
    slug = models.SlugField(default="")
    description = models.TextField(blank=True)
    teaser = models.TextField(blank=True)
    site_url = models.URLField(default="", blank=True)
    demo_url = models.URLField(default="", blank=True)
    display_date = models.CharField(max_length=50, blank=True)
    slot = models.PositiveSmallIntegerField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    type = models.ForeignKey(ProjectType, related_name='projects')

    def __str__(self):
        return self.name

    def full_name(self):
        return "%s %s" % (self.client.name, self.name)

    def type_name(self):
        return self.type.name
    type_name.short_description = "Type"

    def sample_count(self):
        return "%d" % (self.samples.count())
    sample_count.short_description = "Samples"

    def valid_sample_count(self):
        return len([sample for sample in self.samples if self.sample.enabled is True])

    def is_design_related(self):
        return self.type.name in settings.DESIGN_PROJECT_TYPES

    class Meta:
        verbose_name_plural = " Projects"
        ordering = ['slot', ]


class AssetPortfolioManager(models.Manager):
    """Manager to retrieve asset listings on front end portfolio pages."""

    def get_queryset(self):
        return super(AssetPortfolioManager, self).get_queryset()\
            .filter(enabled=True)\
            .order_by('slot')


class Asset(models.Model):
    """Upload files with associated meta data for displaying the
    image in context with information such as caption, description, title, etc."""

    limit = models.Q(app_label='work_projects', model='projectsample') | \
            models.Q(app_label='work_projects', model='gallery')
    content_type = models.ForeignKey(ContentType, default=0, related_name='assets', limit_choices_to=limit)
    object_id = models.PositiveIntegerField(verbose_name='parent', null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(max_length=100, default="")
    slug = models.SlugField(default="")
    image = models.ImageField(upload_to="projects")
    teaser = models.TextField(blank=True)
    caption = models.TextField(blank=True)
    # context = models.CharField(max_length=200, null=True, blank=True)
    slot = models.PositiveIntegerField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag', blank=True)
    objects = models.Manager
    portfolio = AssetPortfolioManager()

    def __str__(self):
        return self.name

    def tags_list(self):
        return [tag.name for tag in self.tags.all()]

    def tag_names(self):
        return ', '.join(self.tags_list())
    tag_names.short_description = "tags"

    def parent_name(self):
        if self.content_object is None:
            return '';
        return self.content_object.name
    parent_name.short_description = 'parent'

    def parent_type(self):
        return self.content_type
    parent_type.short_description = 'parent type'

    class Meta:
        ordering = ['slot', ]


class Tag(models.Model):
    name = models.CharField(max_length=50, default="")
    slug = models.SlugField(default="")

    def __str__(self):
        return self.name


class Gallery(models.Model):
    limit = models.Q(app_label='work_projects', model='projectsample')
    content_type = models.ForeignKey(ContentType, default=0, related_name='galleries', limit_choices_to=limit)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(max_length=100, default="")
    slug = models.SlugField(default="")
    description = models.TextField(blank=True)
    assets = GenericRelation(Asset)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    def related_name(self):
        """ Label used for autocomplete results in related objects admin pages

        :return: gallery identifier
        :rtype: str or unicode
        """
        return self.name

    def asset_count(self):
        return self.assets.count()
    asset_count.short_description = "assets"

    def tags_list(self):
        return [tag.name for tag in self.tags.all()]

    def tag_names(self):
        return ', '.join(self.tags_list())
    tag_names.short_description= "tags"

    def parent_name(self):
        return self.content_object.name
    parent_name.short_description = "parent"

    def parent_type(self):
        return self.content_type.name
    parent_type.short_description = "parent type"

    @staticmethod
    def autocomplete_search_fields():
        return "id__iexact", "name__icontains",

    class Meta:
        verbose_name_plural = "galleries"


class ProjectSampleFrontEndManager(models.Manager):
    def get_queryset(self):
        return super(ProjectSampleFrontEndManager, self).get_queryset()\
            .filter(enabled=True)\
            .order_by('slot')


class ProjectSample(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, related_name='samples')
    slot = models.PositiveIntegerField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    assets = GenericRelation(Asset)
    galleries = GenericRelation(Gallery)
    objects = models.Manager
    frontend = ProjectSampleFrontEndManager()

    def __str__(self):
        return self.name

    def related_label(self):
        """ String displayed in autocomplete results for related objects, e.g. assets """
        return "%s > %s" % (self.project.name, self.name)

    def project_full_name(self):
        return self.project.full_name()
    project_full_name.short_description = "Project"

    def project_full_path(self):
        return "%s > %s > %s" % (self.project.type.name, self.project.name, self.name)
    project_full_path.short_description = "Project"

    def gallery_count(self):
        return "%d" % self.galleries.count()
    gallery_count.short_description = "Galleries"

    def asset_count(self):
        return "%d" % self.assets.count()
    asset_count.short_description = "Assets"

    @staticmethod
    def autocomplete_search_fields():
        return "id__iexact", "name__icontains",

    class Meta:
        ordering = ['slot', ]
