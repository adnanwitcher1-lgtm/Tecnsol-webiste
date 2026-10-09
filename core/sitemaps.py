from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Project, Service


class StaticViewSitemap(Sitemap):
    """Fixed pages of the site."""
    protocol = 'https'
    changefreq = 'monthly'

    _priorities = {
        'core:home': 1.0,
        'core:services': 0.9,
        'core:projects': 0.8,
        'core:contact': 0.8,
        'core:about': 0.7,
        'core:tech_stack': 0.6,
        'core:testimonials': 0.6,
    }

    def items(self):
        return list(self._priorities.keys())

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self._priorities[item]


class ServiceSitemap(Sitemap):
    """One URL per service / course detail page."""
    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Service.objects.all()

    def location(self, obj):
        return reverse('core:service_detail', args=[obj.slug])


class ProjectSitemap(Sitemap):
    """One URL per project detail page."""
    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('core:project_detail', args=[obj.slug])


sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'projects': ProjectSitemap,
}