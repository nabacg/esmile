from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #MAIN app handling
    
    #joke server services ;)
    url(r'jokes/add/$', 'jokeserver.views.add', name='add_joke'),
    url(r'jokes/get/$', 'jokeserver.views.get', name='get_jokes'), 

    #main pages part
    url(r'unsubscribe/$', 'main.views.unsubscribe', name='unsubscribe'),
    url(r'subscribers/$', 'main.views.get_subscribers', name='get_subscribers'),
    url(r'subscribe/$', 'main.views.subscribe', name='subscribe_listener'),  #<= kolejnosc subscribere' methods ma znaczenie
    url(r'(?P<username>.*)/last/joke', 'main.views.user_main', name='user_page'),
    url(r'(?P<user>.*)/tells/joke', 'main.views.teller_main', name='teller_page'),
    url(r'jokes/upvote/(?P<joke_id>[0-9].*)', 'main.views.joke_vote_up', name='up_vote_joke'),
    url(r'jokes/downvote/(?P<joke_id>[0-9].*)', 'main.views.joke_vote_down', name='down_vote_joke'),
    
    #LOGIN and LOGOUT
    url(r'user/logout/$', 'main.views.logout_user', name='logout'),
    url(r'user/login/$', 'main.views.login_user', name='login'),
    url(r'user/register/$', 'main.views.register_user', name="register"),
    url(r'user/edit/$', 'main.views.edit_user', name='edit_user'),
    url(r'user/edit/password/$', 'main.views.change_password', name='change_password'),
    
    #Main index view
    url(r'^$', 'main.views.index', name='index'),
    # Uncomment the next line to enable the admin:
     (r'^library/', include(admin.site.urls)),
    (r'site_media/(?P<path>[a-zA-Z0-9].*)$', 'django.views.static.serve', {'document_root': settings.STATIC_MEDIA_ROOT}),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'site_media/(?P<path>[a-zA-Z0-9].*)$', 'django.views.static.serve', {'document_root': settings.STATIC_MEDIA_ROOT}),
    )