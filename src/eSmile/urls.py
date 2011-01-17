from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #MAIN app handling
    
    #joke server services ;)
    url(r'jokes/add/$', 'eSmile.jokeserver.views.add', name='add_joke'),
    url(r'jokes/get/$', 'eSmile.jokeserver.views.get', name='get_jokes'), 

    #main pages part
    url(r'unsubscribe/$', 'eSmile.main.views.unsubscribe', name='unsubscriber'),
    url(r'subscribers/$', 'eSmile.main.views.get_subscribers', name='get_subscribers'),
    url(r'subscribe/$', 'eSmile.main.views.subscribe', name='subscribe_listener'),  #<= kolejnosc subscribere' methods ma znaczenie
    url(r'(?P<username>.*)/last/joke', 'eSmile.main.views.user_main', name='user_page'),
    url(r'(?P<username>.*)/tells/joke', 'eSmile.main.views.teller_main', name='teller_page'),
    
    #LOGIN and LOGOUT
    url(r'user/logout/$', 'eSmile.main.views.logout_user', name='logout'),
    url(r'user/login/$', 'eSmile.main.views.login_user', name='login'),
    
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