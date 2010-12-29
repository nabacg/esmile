from django.contrib import admin
from eSmile.jokeserver.models import Joke, Subscriber, ReceivedJoke

class JokeAdmin(admin.ModelAdmin):
#    value = models.TextField()
#    owner = models.ForeignKey(User, related_name = 'jokes')
#    date_created = models.DateTimeField(auto_now_add = True)
#    date_last_update = models.DateTimeField(auto_now=True)
#    sent = models.BooleanField(default=False)
    
    list_filter = ('sent', 'owner')
    list_display  = ('owner', 'date_created', 'date_last_update', 'sent', 'value')
    search_fields = ['owner__email', 'owner__username', 'value']

admin.site.register(Joke, JokeAdmin)

class SubscriberAdmin(admin.ModelAdmin):
    pass

admin.site.register(Subscriber, SubscriberAdmin)

class ReceivedJokeAdmin(admin.ModelAdmin):
    list_filter = ('send', 'like_id')
    list_display  = ('send', 'date_send', 'joke')
    search_fields = ['owner__email',  'joke__value']

admin.site.register(ReceivedJoke, ReceivedJokeAdmin)