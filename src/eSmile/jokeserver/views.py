# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.utils import simplejson
from eSmile.jokeserver import jokefacade

extract_joke = lambda j: { "value": j.value, "datePosted": j.date_created.strftime('%Y-%m-%d %H:%M:%S') }

def get(request):
    if request.method == "POST":
        params =  request.POST
    else:
        params =  request.GET
    teller_username = params["jokeTeller"] 
    return HttpResponse(
            simplejson.dumps( 
                map(  extract_joke, 
                     jokefacade.get_teller_jokes(teller_username))))
    
def add(request):
    if request.method == "POST":
        params =  request.POST
    else:
        params =  request.GET
    teller_username = params["jokeTeller"]
    joke_value = params["jokeValue"]
    joke_value = joke_value.replace('\n', '<br/>')
    
    return HttpResponse(simplejson.dumps({ 
                     "success": True,
                     "joke": extract_joke(jokefacade.add_new_joke(teller_username, joke_value))                              
                     }))

    
