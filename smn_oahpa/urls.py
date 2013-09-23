from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.conf import settings

import os, sys
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x)


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from settings import URL_PREFIX as prefix

admin_url = r'^%s/admin/' % prefix

urlpatterns = patterns('',
	# Example:
	# (r'^smn_oahpa/', include('smn_oahpa.foo.urls')),
	url(r'^%s/$' % prefix, 'smn_oahpa.smn_drill.views.index'),
	url(r'^%s/i18n/' % prefix, include('django.conf.urls.i18n')),
	url(r'^%s/media/(?P<path>.*)$' % prefix, 'django.views.static.serve',
			  	{'document_root': settings.MEDIA_ROOT}),
	url(r'^%s/courses/' % prefix, include('smn_oahpa.courses.urls')),
	url(r'^%s/' % prefix, include('smn_oahpa.smn_drill.urls')),
	url(r'^%s/dialect/$' % prefix, 'smn_oahpa.conf.views.dialect'),
	url(admin_url, include(admin.site.urls)),
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	#url(r'^%s/openid/' % prefix, include('smn_oahpa.openid_provider.urls')),
)

