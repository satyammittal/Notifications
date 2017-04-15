from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'notifier.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^subscribe/', include('notification.urls')),
    url(r'^notify/', include('notification.urls')),
    url(r'^unsubscribe/', include('notification.urls')),
    url(r'^subscribe2/', include('notification.urls')),
    url(r'^updatestocks/', include('notification.urls')),
    url(r'^updatevalue/', include('notification.urls')),
)
