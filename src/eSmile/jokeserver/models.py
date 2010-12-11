from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save

class Joke(models.Model):
    value = models.TextField()
    owner = models.ForeignKey(User, related_name = 'jokes')
    date_created = models.DateTimeField(auto_now_add = True)
    date_last_update = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s: %s" % (self.owner.username, self.value)
    
#SUbscribers maybe?
class Subscriber(models.Model):
    teller = models.ForeignKey(User, related_name = 'joke_listeners')
    listener = models.ForeignKey(User, related_name = 'joke_tellers')
    date_assigned = models.DateTimeField(auto_now_add = True);
    received_jokes = models.ManyToManyField(Joke, through = 'ReceivedJoke')
    
    
    def get_listener_email(self):
        return self.listener.email
    
    receiver_email = property(get_listener_email)
    
    def __unicode__(self):
        return '%s owns %s' % (self.teller.username, self.listener.username)
    

    
# Subscribtions?
class ReceivedJoke(models.Model):
    subscriber = models.ForeignKey(Subscriber)
    joke = models.ForeignKey(Joke)
    send = models.BooleanField(default = False)
    like_id = models.BooleanField()
    date_send = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return '%s will be send to %s'%(self.joke.value, self.subscriber.receiver_email)
    
    def create_received_joke(sender, instance, created, **kwargs):
        if created:
            for subsc in instance.owner.joke_listeners.all():
                ReceivedJoke.objects.get_or_create(joke = instance, subscriber = subsc)

    post_save.connect(create_received_joke, sender=Joke)