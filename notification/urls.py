from django.conf.urls import patterns, url
from notification import views

urlpatterns = patterns('',
        url(r'^login/$', views.user_login, name='login'),
        url(r'^home/$', views.home, name='home'),
        url(r'^subscribe/$', views.subscribe, name='subscribe'),
        url(r'^unsubscribe/$', views.unsubscribe, name='unsubscribe'),
        url(r'^subscribe2/$', views.subscribe2, name='subscribe2'),
        url(r'^updatestocks/$', views.update, name='update'),
        url(r'^updatevalue/$', views.updatevalue, name='updatevalue'),
        url(r'^$', views.index, name='index'),
       
        )