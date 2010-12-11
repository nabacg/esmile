from django.core.mail import send_mail
from eSmile.jokeserver.models import Subscriber, ReceivedJoke
from eSmile.jokeserver import jokefacade
from django.conf import settings
from django.template import Template, Context

def send_joke(joke, receiver_list):
    result_status = send_mail(get_email_subject(joke), get_email_content(joke), settings.DEFAULT_FROM_EMAIL, receiver_list)
#    print "RESULT STATUS %d" % result_status
    if result_status != 1:
        raise NameError("Can send god damn email, meen.")
 
# tutaj trzeba zaprzadz django-template'y w towrzenie ladnego maila
def get_email_content(joke):
     new_email = Template("{{ user_name }} joke for today:\n\n {{ joke_text }} \n\n\n \t\t\t posted on {{ posted_on }} \n\n\n------------------------------------------------------------------------------------------------------\n\n \t\t\t This joke was delivered to you using {{esmile_url}}")
     context = Context({
                        "user_name": joke.owner.username,
                        "joke_text": joke.value.replace('<br/>', '\n'),
                        "posted_on": joke.date_created,
                        "esmile_url": "www.esmile.gmc.megiteam.pl/%s/last/joke" % joke.owner.username 
                        })
     return new_email.render(context)
 
#     return %(joke.value, str(joke.date_created))
 
def get_email_subject(joke):
    return "SMILE: %s's Daily joke!"%joke.owner.username

 #probably refactor to separate class, SendingQueue 
 # might also make sense to store it somewhere, like DB and just get it back and send send newest ones..  
def queue_joke(joke_queue, joke, receivers):
    teller = joke.owner.username
    if joke_queue.get(teller) == None:
        joke_queue[teller] = { "joke": joke, "receivers": receivers }
    
def send_daily_jokes():
    joke_teller_queue = {} # { "joke_teller_name": {"joke": joke_object:,  "receiver_list": list}
    
    for joke in jokefacade.get_jokes_to_send(): 
        receiver_list = map(lambda r: str(r.receiver_email), joke.owner.joke_listeners.all())
        queue_joke(joke_teller_queue, joke, receiver_list)
        
    for teller in joke_teller_queue.keys():
        msg = joke_teller_queue[teller]
        try:
            status = send_joke(msg['joke'], msg['receivers'])          
        except Exception:
            status = -1
            
        if status != -1:    
            for rj in ReceivedJoke.objects.filter(joke = msg['joke']): # to nie dziala
                rj.send = True
                rj.save()
                print "We did save some RJ's"
            
