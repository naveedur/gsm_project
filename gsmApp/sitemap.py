from django.contrib.sitemaps import Sitemap
from.models import *


class brandsitemap(Sitemap):
    changefreq='hourly'
    priority=0.9

    def items(self):
        return brand.objects.all()
 
    def location(self,obj):
        return '/models/%s' % (obj.title)



class modelsitemap(Sitemap):
    changefreq='hourly'
    priority=0.9

    def items(self):
        return model.objects.all()
 
    def location(self,obj):
        return '/resources/%s' % (obj.title)        

class resourcesitemap(Sitemap):
    changefreq='hourly'
    priority=0.9

    def items(self):
        return resource.objects.all()
 
    def location(self,obj):
        return '/download/%s' % (obj.title)          


