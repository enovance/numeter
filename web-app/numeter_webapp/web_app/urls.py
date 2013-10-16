"""
Base urls file.
"""
from django.conf import settings as s
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'core.views.views.index', name='index'),
    url(r'^apropos$', 'core.views.views.apropos', name='apropos'),
    url(r'^login$', 'core.views.auth.login', name='login'),
    url(r'^logout$', 'core.views.auth.logout', name='logout'),
    # Profile
    url(r'^profile$', 'core.views.profile.modal', name='profile'),
    url(r'^profile/(?P<user_id>\d+)$', 'core.views.profile.update', name='profile update'),
    url(r'^profile/(?P<user_id>\d+)$', 'core.views.profile.update', name='profile update'),
    url(r'^profile/(?P<user_id>\d+)/password$', 'core.views.profile.password', name='profile password'),
    # Graph
    url(r'^get/graph/(?P<host_id>\d+)/(?P<plugin>.+)$', 'core.views.hosttree.get_data', name='plugin'),
    # Hosttree
    url(r'^hosttree/group/(?P<group_id>\d+)?$', 'core.views.hosttree.group', name= 'hosttree group'),
    url(r'^hosttree/host/(?P<host_id>\d+)$', 'core.views.hosttree.host', name='hosttree host'),
    url(r'^hosttree/category/(?P<host_id>\d+)$', 'core.views.hosttree.category', name='hosttree category'),
    # Includes
    url(r'^multiviews/', include('multiviews.urls')),
    url(r'^configuration/', include('configuration.urls')),
    url(r'^', include('rest.urls')),
    # Files
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': s.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': s.MEDIA_ROOT}),
)

# Include mock storage
if 'mock_storage' in s.INSTALLED_APPS:
    urlpatterns = patterns('', url(r'^mock/', include('mock_storage.urls')), *list(urlpatterns))
