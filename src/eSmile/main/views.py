# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response
from jokeserver import notificationfacade
from jokeserver.models import Joke
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,\
    PasswordChangeForm
from django.template import RequestContext
from jokeserver import subscriberfacade, jokefacade
from django.utils import simplejson
from django.contrib.auth import login, authenticate
from main import userfacade
from django.contrib.auth.decorators import login_required
from main.forms import UserEditForm

def index(request):
    return render_to_response('main.html', 
                              {"latest_jokes": jokefacade.get_latest_jokes(),
                               "most_active_tellers":  userfacade.get_most_active_users()}, context_instance=RequestContext(request))


def user_main(request, username):
    user = get_object_or_404(User, username=username)
    return render_to_response('user.html', {"username": user.username}, context_instance=RequestContext(request))

@login_required
def teller_main(request, user):
    if not hasattr(user, 'username'): # sie znaczy przekazano nie usera a username
        user = r = get_object_or_404(User, username=user)
    return render_to_response('teller.html', {"username": user.username, "logged": True}, context_instance=RequestContext(request))

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
                return redirect('teller_page', user = user.username)
        else:
            error_msg = "Wrong login or password"
    #jeze;o nie udalo sie zalogowac albo dopiero wchodzimy na strone logowania to zwracamy pusty formuarz
    return render_to_response('login.html', 
                              {"form" : AuthenticationForm(), "form.errors": error_msg}, 
                              context_instance=RequestContext(request)) 
            
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('login')
        
    else:
        form = UserCreationForm()

    return render_to_response("login.html", {
        'register_form' : form
    }, context_instance=RequestContext(request))
    
@login_required    
def edit_user(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance= request.user)
        if form.is_valid():
            form.save()
    else:
        form = UserEditForm(instance = request.user)
        
    return render_to_response('user_edit.html', 
                              {'edit_form': form}, 
                              context_instance = RequestContext(request))

@login_required    
def change_password(request):
    if request.method == 'POST':       
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(request.POST['new_password1'])
            request.user.save()
            redirect('edit_form')
    else:
        form = PasswordChangeForm(request.user)
        
    return render_to_response('change_password.html',
                              {'password_form': form},
                              context_instance = RequestContext(request))
