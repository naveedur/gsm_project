
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from gsmApp.sitemap import *
sitemaps={
    'resource':resourcesitemap,
    'brand':brandsitemap,
    'model':modelsitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gsmApp.urls')),
    path('blog/', include('blogApp.urls')),
    path('subscription/',include('subscriptionApp.urls')),
    path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),
    # path('paypal/', include('paypal.standard.ipn.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap')
  
]
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# summernotes
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
