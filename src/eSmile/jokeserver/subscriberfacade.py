from jokeserver.models import User, Subscriber, ReceivedJoke

def get_subscribers(teller):
    if not hasattr(teller, 'username'):
        teller = User.objects.get(username = teller) 
    subscribtions = teller.joke_listeners.all()
    return map(lambda s: s.listener, subscribtions)

def unsubscribe(teller, listener_username): 
    if not hasattr(teller, 'username'):
        teller = User.objects.get(username = teller)
        
    if hasattr(listener_username, 'username'):
        listener_username = listener.username
    teller.joke_listeners.filter(listener__username = listener_username).delete()


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
        new_user = User(username = subscriber_email, email = subscriber_email)
        new_user.set_password(subscriber_email)
        new_user.save()
        return new_user
    else:
        return matchin_users[0]