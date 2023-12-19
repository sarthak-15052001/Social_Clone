from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
# Create your models here.
User = get_user_model()
register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)       #The SlugField is a field for storing slugs, which are short labels that contain only letters, numbers, underscores, or hyphens. The allow_unicode=True parameter ensures that the slug can contain non-ASCII characters as well. The unique=True parameter ensures that each slug in the database is unique.
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):                             # In the save method of the Group model, the slugify function is used to automatically generate the slug from the name field. This function converts the name into a slug by replacing spaces with hyphens, converting all characters to lowercase, and removing any characters that are not alphanumeric, underscores, or hyphens.
        self.slug = slugify(self.name)                           # The usage of the SlugField and the slugify function in this context helps in creating clean and SEO-friendly URLs for each group. This can improve the visibility of the web pages in search engines and make the URLs more human-readable and shareable.
        self.description_html = mark_safe(self.description)      # In Django, the mark_safe function is used to explicitly mark a string as safe for HTML output. This function is used to indicate to the template engine that the content of the string should be treated as safe HTML and not escaped.                                            
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['name']
    

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_groups')


    def __str__(self):
        return self.user.username


    class Meta:
        unique_together = ('group', 'user')
    