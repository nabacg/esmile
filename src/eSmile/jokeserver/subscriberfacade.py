from eSmile.jokeserver.models import User, Subscriber, ReceivedJoke

def get_subscribers(teller):
    if not hasattr(teller, 'username'):
        teller = User.objects.get(username = teller) 
    subscribtions = teller.joke_listeners.all()
    return map(lambda s: s.listener, subscribtions)

def subscribe(teller, subscriber):
    if not hasattr(teller, 'username'):
        teller = User.objects.get(username = teller)
    if not hasattr(subscriber, 'username'):
        subscriber = get_or_create_subscriber(subscriber)
    new_subscriber = Subscriber(teller = teller, listener = subscriber)
    
    
    if not new_subscriber in subscriber.joke_tellers.all():
        new_subscriber.save()
    set_un_received_jokes_for_new_subscriber(teller, new_subscriber)
#        Subscriber.objects.create(teller = teller, listener = subscriber)

def set_un_received_jokes_for_new_subscriber(teller, subscriber):
    for joke in teller.jokes.all():
        ReceivedJoke.objects.get_or_create(joke = joke, subscriber = subscriber)

def get_or_create_subscriber(subscriber_email):
    matchin_users = User.objects.filter(email = subscriber_email)
    if len(matchin_users) == 0:
        return User.objects.create(username = subscriber_email, email = subscriber_email, password = subscriber_email)
    else:
        return matchin_users[0]