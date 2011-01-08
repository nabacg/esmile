# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response
from eSmile.jokeserver import notificationfacade
from eSmile.jokeserver.models import Joke
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def index(request):
    return render_to_response('index.html')


def user_main(request, username):
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    user = get_object_or_404(User, username=username)
    return render_to_response('user.html', {"username": user.username, "logged": logged})

def send_mail(request):
    for joke in Joke.objects.all().order_by('date_created'):#[0]#(value = JOKE_3)
        teller = joke.owner
        receiver_list = map(lambda r: str(r.receiver_email), teller.joke_listeners.all())
        print receiver_list
        notificationfacade.send_joke(joke, receiver_list)
    
    return HttpResponse("")