from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #MAIN app handling
    
    #joke server services ;)
    (r'jokes/add/$', 'eSmile.jokeserver.views.add'),
    (r'jokes/get/$', 'eSmile.jokeserver.views.get'), 

    #main pages part
    (r'subscribe/$', 'eSmile.main.views.subscribe'),
    (r'(?P<username>.*)/last/joke', 'eSmile.main.views.user_main'),
    (r'send/mail/$', 'eSmile.main.views.send_mail'),
    
    #LOGIN and LOGOUT
    (r'user/logout/$', 'eSmile.main.views.logout_user'),
    (r'user/login/$', 'eSmile.main.views.login_user'),
    
    #(r'^sign/$', 'eSmile.main.views.sign_up'),
    
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