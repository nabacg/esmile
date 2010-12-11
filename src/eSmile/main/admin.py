from django.contrib import admin
from eSmile.jokeserver.models import Joke, Subscriber, ReceivedJoke

class JokeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Joke, JokeAdmin)

class SubscriberAdmin(admin.ModelAdmin):
    pass

admin.site.register(Subscriber, SubscriberAdmin)

class ReceivedJokeAdmin(admin.ModelAdmin):
    pass

admin.site.register(ReceivedJoke, ReceivedJokeAdmin)