# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response
from eSmile.jokeserver import notificationfacade
from eSmile.jokeserver.models import Joke
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext
from eSmile.jokeserver import subscriberfacade
from django.utils import simplejson
from django.contrib.auth import login, authenticate

def index(request):
    return render_to_response('index.html')


def user_main(request, username):
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    user = get_object_or_404(User, username=username)
    return render_to_response('user.html', {"username": user.username, "logged": logged})

def teller_main(request, user):
    if not hasattr(user, 'username'): # sie znaczy przekazano nie usera a username
        user = r = get_object_or_404(User, username=user)
    return render_to_response('teller.html', {"username": user.username, "logged": True})

def send_mail(request):
    for joke in Joke.objects.all().order_by('date_created'):#[0]#(value = JOKE_3)
        teller = joke.owner
        receiver_list = map(lambda r: str(r.receiver_email), teller.joke_listeners.all())
        print receiver_list
        notificationfacade.send_joke(joke, receiver_list)
    
    return HttpResponse("")

def subscribe(request):
    if request.method == "POST":
        params =  request.POST
    else:
        params =  request.GET
    teller_username = params['tellerUsername']
    subscriber_email = params['subscriberEmail']    
    try:
        subscriberfacade.subscribe(teller = teller_username, subscriber = subscriber_email)
        return HttpResponse(simplejson.dumps({ "success": True }));
    except Exception as e:
        return HttpResponse(simplejson.dumps({"success": False, "errormsg": e}))
    
def unsubscribe(request):    
    if request.method == "POST":
        params =  request.POST
    else:
        params =  request.GET
    teller_username = params['tellerUsername']
    subscriber_username = params['subscriberUsername'] 
    try:
        subscriberfacade.unsubscribe(teller = teller_username, listener_username=subscriber_username)
        return HttpResponse(simplejson.dumps({ "success": True }));
    except Exception as e:
        return HttpResponse(simplejson.dumps({"success": False, "errormsg": e}))
    
def get_subscribers(request):
    if request.method == "POST":
        params =  request.POST
    else:
        params =  request.GET
    teller_username = params['tellerUsername']
    return HttpResponse(simplejson.dumps({ "success": True, 
                                          "data": map(lambda u: u.username, subscriberfacade.get_subscribers(teller_username))}))
    
def logout_user(request):
    logout(request)
    return render_to_response('login.html', {"form" : AuthenticationForm()}, context_instance=RequestContext(request))

def login_user(request):
    error_msg = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return teller_main(request, user = user)
        else:
            error_msg = "Wrong login or password"
    #jeze;o nie udalo sie zalogowac albo dopiero wchodzimy na strone logowania to zwracamy pusty formuarz
    return render_to_response('login.html', {"form" : AuthenticationForm(), "form.errors": error_msg}, context_instance=RequestContext(request)) 
            

    

