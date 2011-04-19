# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.utils import simplejson
from jokeserver import jokefacade

extract_joke = lambda j: { "value": j.value, "datePosted": j.date_created.strftime('%Y-%m-%d %H:%M:%S'), "sent": j.sent }

def get(request):
    if request.method == "POST":
        params =  request.POST
    else:
        params =  request.GET
    teller_username = params["jokeTeller"] 
    is_owner = request.user.is_authenticated() and request.user.username == teller_username
    return HttpResponse(
            simplejson.dumps( 
                map(  extract_joke, 
                     jokefacade.get_teller_jokes(teller_username, only_sent = not is_owner))))
    
def add(request):
    if request.method == "POST":
        params =  request.POST
    else:
        params =  request.GET
    teller_username = params["jokeTeller"]
    joke_value = params["jokeValue"]
    #joke_value = joke_value.replace('\n', '<br/>')
    
    return HttpResponse(simplejson.dumps({ 
                     "success": True,
                     "joke": map(extract_joke, jokefacade.add_new_jokes(teller_username, joke_value))                              
                     }))

    
