from jokeserver.models import *


def get_latest_jokes():
    return Joke.objects.order_by('-date_created')[0: 10]

def get_teller_jokes(teller_name, only_sent = True):
    joke_set = Joke.objects.all()#.filter(receivedjoke__send=True).distinct()
    if only_sent:
        joke_set = joke_set.filter(sent = True)
    joke_set = joke_set.filter(owner__username=teller_name) | joke_set.filter(owner__email=teller_name)
#    assert False
    return joke_set.order_by('-date_created')
#    return Joke.objects.filter(owner__username = teller_name).order_by('-date_created')

def add_new_jokes(teller, jokes_text):
    if not hasattr(teller, 'username'):
        teller = User.objects.get(username=teller)
    new_jokes = []
    #assert False
    for joke in jokes_text.split('<br/><br/><br/>'):
        new_jokes.append(add_new_joke(teller, joke))
    return new_jokes

def add_new_joke(teller, joke_text):
    if not hasattr(teller, 'username'):
        teller = User.objects.get(username=teller)
    return teller.jokes.create(value=joke_text)

def get_jokes_to_send():
    # we wanna send older one first
    return Joke.objects.filter(sent = False).order_by('date_created') #.filter(receivedjoke__send=False).distinct()

