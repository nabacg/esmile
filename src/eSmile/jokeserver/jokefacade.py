from eSmile.jokeserver.models import *

def get_teller_jokes(teller_name):
    joke_set = Joke.objects.filter(receivedjoke__send = True).distinct()
    joke_set = joke_set.filter(owner__username = teller_name) | joke_set.filter(owner__email = teller_name)
    return joke_set.order_by('-date_created')
#    return Joke.objects.filter(owner__username = teller_name).order_by('-date_created')

def add_new_joke(teller_username, joke_text):
    teller = User.objects.get(username= teller_username)
    return teller.jokes.create(value = joke_text)

def get_jokes_to_send():
    return Joke.objects.filter(receivedjoke__send = False).order_by('date_created')# we wanna send older one first