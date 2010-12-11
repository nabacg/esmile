from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #joke server services ;)
    (r'subscribe/$', 'eSmile.jokeserver.views.subscribe'),
    (r'jokes/add/$', 'eSmile.jokeserver.views.add'),
    (r'jokes/get/$', 'eSmile.jokeserver.views.get'), # to sie musi nazywac /jokes/get/ sorry

    #main pages part
#    (r'main/$', 'eSmile.main.views.index'),
    (r'(?P<username>.*)/last/joke', 'eSmile.main.views.user_main'),
    (r'send/mail/$', 'eSmile.main.views.send_mail'),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
    (r'site_media/(?P<path>[a-zA-Z0-9].*)$', 'django.views.static.serve', {'document_root': settings.STATIC_MEDIA_ROOT}),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'site_media/(?P<path>[a-zA-Z0-9].*)$', 'django.views.static.serve', {'document_root': settings.STATIC_MEDIA_ROOT}),
    )