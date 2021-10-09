from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 1 # importance
    protocol = "https"

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.published_date

class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['/about']

    def location(self, item):
        return item
