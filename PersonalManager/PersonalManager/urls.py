from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PersonalManager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'ManagerApp.views.home', name=''),
    url(r'index.html$', 'ManagerApp.views.home', name=''),
    url(r'^admin/', include(admin.site.urls)),
)
