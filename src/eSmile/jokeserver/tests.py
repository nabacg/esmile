"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from eSmile.jokeserver.models import *
#from eSmile.jokeserver.jokefacade import get_teller_jokes
from eSmile.jokeserver import jokefacade, subscriberfacade, notificationfacade
import time
from django.test.client import Client
from django.core.urlresolvers import reverse

TELLER_NAME = "JOE THE JOKE TELLER"
LISTENER_1 = "Mary, likes policemen jokes"
LISTENER_2 = "Johnny the rasist" 
PASSWORD = 'dum8pa$$'
EMAIL = "grigoriij@o2.pl"
EMAIL_REAL = 'gmdc.inc@gmail.com'
SUBSCRIBER_EMAIL = 'faithfull@listener.com'
JOKE_1 = 'Tu ti tu rum tu tu'
JOKE_2 = 'Szczyt bezczelnosci? Zaglosowac na PiS i wyjechac..'
JOKE_3 = 'nuuuda'
JOKE_4 = 'Dowcip o policjancie'

def setTestData(test_case):        
    test_case.teller = User.objects.create(username= TELLER_NAME, password = PASSWORD, email = EMAIL)
    test_case.first_listener = User.objects.create(username=LISTENER_1, password=PASSWORD, email=EMAIL)
    test_case.second_listener = User.objects.create(username=LISTENER_2, password=PASSWORD, email=EMAIL_REAL)
    Subscriber.objects.create(teller=test_case.teller, listener=test_case.first_listener)
    Subscriber.objects.create(teller=test_case.teller, listener=test_case.second_listener)
    time.sleep(0.1)
    Joke.objects.create(owner=test_case.teller, value=JOKE_1, sent = True)
    time.sleep(0.1)
    Joke.objects.create(owner=test_case.teller, value=JOKE_2)
    time.sleep(0.1)
    Joke.objects.create(owner=test_case.teller, value=JOKE_3)

    
class DbSchemaTest(TestCase):
    def setUp(self):
        setTestData(self)
        for joke in self.teller.jokes.all():
            ReceivedJoke.objects.create(subscriber = self.first_listener.joke_tellers.all()[0], joke = joke,  send = True)
        
    def test_get_all_joke_listeners(self):
        saved_teller = User.objects.get(username = self.teller.username)
        self.assertEqual(saved_teller.username, self.teller.username, "Teller not saved properly")
        
        listeners = saved_teller.joke_listeners.all().order_by('date_assigned')
        self.assertEqual(2, len(listeners), "Joke listeners list is too short, expecting 2 found %d"% len(listeners))
        self.assertEqual(self.first_listener,  listeners[0].listener, "First listener %s was not assigned"%self.first_listener.username)
        self.assertEqual(self.second_listener, listeners[1].listener, "Second listener %s was not assigned"%self.second_listener.username)
    

    def test_get_joke_tellers_for_listener(self):
        listener = User.objects.get(username = self.second_listener.username)
        tellers = listener.joke_tellers.all()
        self.assertEqual(1, len(tellers), "Joke teller list has wrong length, expected 1 found %d"% len(tellers))
        self.assertEqual(self.teller.username, tellers[0].teller.username, "Joke teller name does not match, %s expected, found %s"%(self.teller.username, tellers[0].teller.username))
    
    def test_get_all_teller_jokes(self):
        joke_list = self.teller.jokes.all().order_by('-date_created')
        self.assertNotEqual(0, len(joke_list), "Joke list can\'t be empty")
        last_date = None
        for joke in joke_list:
            self.assertEqual(self.teller, joke.owner, 
                             "Joke owners not matching, expected %s found %s" % (self.teller.username,
                                                                                 joke.owner.username))
            self.assertNotEqual('', joke.value, "Joke can\' be empty!!")
            if last_date != None:
               self.assertTrue(joke.date_created < last_date, '%s should be after %s'%(str(joke.date_created),str(last_date)))   
            last_date = joke.date_created
    
    def test_add_new_joke(self):
        self.teller.jokes.create(value = JOKE_4)
        saved_joke = Joke.objects.get(value = JOKE_4, owner = self.teller)
        self.assertNotEqual(None, saved_joke, "New joke creation was a joke")
        
    def test_get_subscriber_received_jokes(self):
#        for subscription in self.first_listener.joke_tellers.all(): 
#            for joke in subscription.received_jokes.all():
#                self.assertFalse(joke.send, "Joke wasn\'t supposed to be sent!")
#                
        first_listener_jokes = self.first_listener.joke_tellers.all()[0].received_jokes.filter(receivedjoke__send = True)
        self.assertEqual(3, len(first_listener_jokes), "Wrong number of jokes send.. expecting 3")
        
class JokeFacadeTest(TestCase):
    
    def setUp(self):
        setTestData(self)
           
    def test_get_joke_list(self):
        joke_list = jokefacade.get_teller_jokes(self.teller.username)
        self.assertNotEqual(0, len(joke_list))
        last_date = None
        for joke in joke_list:
            self.assertNotEqual('', joke.value, "Joke can\' be empty!!")
            if last_date != None:
                self.assertTrue(last_date > joke.date_created, '%s should be after %s'%(str(last_date), str(joke.date_created)))   
            last_date = joke.date_created
    
#    def test_create_new_joke(self):
#        joke_text = JOKE_4
#        new_joke = jokefacade.add_new_joke(self.teller.username, joke_text)
#        self.assertNotEqual(None, new_joke, "New joke not created properly")
#        new_joke_list = jokefacade.get_teller_jokes(self.teller.username)
#        self.assertTrue(new_joke in new_joke_list, "New joke not added to teller list")
 
class SubscriberFacadeTest(TestCase):
    
    def setUp(self):
        setTestData(self)       
        
    def test_subscribe_new_user(self):
        user_list = User.objects.filter(email = SUBSCRIBER_EMAIL)
        self.assertEqual(0, len(user_list), "Can\'t test, user %s already exists!"%SUBSCRIBER_EMAIL)
        subscriberfacade.subscribe(self.teller, SUBSCRIBER_EMAIL)
        
        
        #check if there is a new user 
        new_user = User.objects.get(email = SUBSCRIBER_EMAIL)
        self.assertEqual(new_user.username, SUBSCRIBER_EMAIL)
        subscriptions = new_user.joke_tellers.filter(teller__username = self.teller.username)
        self.assertNotEqual(0, len(subscriptions), "New user not assigned to test teller!")
        
        #check if test teller has new subscriber
        listener_list = Subscriber.objects.filter(teller = self.teller)
        listener_found = False
        for listener in listener_list:
            if listener.listener.username == SUBSCRIBER_EMAIL:
                listener_found = True
                
        self.assertTrue(listener_found, "New subscriber was not found in %s list"%self.teller.username) 
        
    def test_subscribe_existing_user(self):
        existing_user = User.objects.all()[0]
        self.assertNotEqual(None, existing_user, "Existing user %s not found, can'\t perform the test!"%SUBSCRIBER_EMAIL)
        
        subscriberfacade.subscribe(self.teller, existing_user)
        user_list = User.objects.filter(username = existing_user.username)
#        print len(user_list)
        self.assertEqual(1, len(user_list), "There is a new user with %s email created after subscribing existing user to teller %s"%(existing_user.email, self.teller.username))
        
        subscriptions = existing_user.joke_tellers.filter(teller__username = self.teller.username)
        self.assertNotEqual(0, len(subscriptions), "New user not assigned to test teller!")
        found = False
        
        for subsc in subscriptions:
            if subsc.teller.username == self.teller.username:
                found = True
                
        self.assertTrue(found, "Subscribed Teller %s not found in user %s subscribtions"%(self.teller.username, existing_user.username))
        
    def test_subscribe_new_user_by_username(self): #ie string usernames not objects
        user_list = User.objects.filter(email = SUBSCRIBER_EMAIL)
        self.assertEqual(0, len(user_list), "Can\'t test, user %s already exists!"%SUBSCRIBER_EMAIL)
        subscriberfacade.subscribe(self.teller.username, SUBSCRIBER_EMAIL)
        
        
        #check if there is a new user 
        new_user = User.objects.get(email = SUBSCRIBER_EMAIL)
        self.assertEqual(new_user.username, SUBSCRIBER_EMAIL)
        subscriptions = new_user.joke_tellers.filter(teller__username = self.teller.username)
        self.assertNotEqual(0, len(subscriptions), "New user not assigned to test teller!")
        
        #check if test teller has new subscriber
        listener_list = Subscriber.objects.filter(teller = self.teller)
        listener_found = False
        for listener in listener_list:
            if listener.listener.username == SUBSCRIBER_EMAIL:
                listener_found = True
                
        self.assertTrue(listener_found, "New subscriber was not found in %s list"%self.teller.username) 
     
    def test_subscribe_existings_user_by_username(self):
        existing_user = User.objects.all()[0]
        self.assertNotEqual(None, existing_user, "Existing user %s not found, can'\t perform the test!"%SUBSCRIBER_EMAIL)
        
        subscriberfacade.subscribe(self.teller.username, existing_user.email)
        user_list = User.objects.filter(username = existing_user.username)
#        print len(user_list)
        self.assertEqual(1, len(user_list), "There is a new user with %s email created after subscribing existing user to teller %s"%(existing_user.email, self.teller.username))
        
        subscriptions = existing_user.joke_tellers.filter(teller__username = self.teller.username)
        self.assertNotEqual(0, len(subscriptions), "New user not assigned to test teller!")
        found = False
        
        for subsc in subscriptions:
            if subsc.teller.username == self.teller.username:
                found = True
                
        self.assertTrue(found, "Subscribed Teller %s not found in user %s subscribtions"%(self.teller.username, existing_user.username))
                    
    def tearDown(self):
        User.objects.filter(email = SUBSCRIBER_EMAIL).delete()
        
class NotificationServiceTest(TestCase):

    def setUp(self):
        setTestData(self)
        for joke in self.teller.jokes.all():
            ReceivedJoke.objects.create(subscriber = self.second_listener.joke_tellers.all()[0], joke = joke,  send = False)
      
        
    def test_send_sample_joke(self):
        joke = Joke.objects.get(value = JOKE_3)
        teller = joke.owner
        receiver_list = map(lambda r: str(r.receiver_email), teller.joke_listeners.all())
#        print receiver_list
        notificationfacade.send_joke(joke, receiver_list)
        
    def test_get_email_content(self):
        joke = Joke.objects.get(value = JOKE_3)
        email = notificationfacade.get_email_content(joke)
        print email
        
        
    def test_send_daily_joke(self):
        notificationfacade.send_daily_jokes()   
        #send joke to listener 2
#        print ReceivedJoke.objects.filter(send = False)
#        for subscribed in self.second_listener.joke_tellers.all(): #grr joke_teller to tak naprawde subscritions... 
#            for joke in subscribed.received_jokes.filter(receivedjoke__send = False):
#                print joke
#                notificationfacade.send_joke(self.second_listener, joke)
#                self.assertTrue(joke.receivedjoke.send, "Send flag not fliped")
                
#        for subscr in Subscriber.object.filter(listener = self.second_listener):
#            for joke in subscr.received_joke.filter(received_send = False):
#                notificationfacade.send_joke(self.second_listener.email, joke)
#                self.assertTrue(joke.receivedjoke.send, "Send flag not fliped")
        
class JokeServerTest(TestCase):
    
    def setUp(self):
        setTestData(self)
        self.client = Client()
       
    def test_get_json_joke_list(self):
        response = self.client.get(reverse('eSmile.jokeserver.views.get'),data={"jokeTeller": self.teller.username})# args={self.teller.username:self.teller.username})) #'/jokes/user'
        expected_status = 200
        self.assertEqual(expected_status, response.status_code, "Wrong Http response status code, %d expected"%expected_status)
        content = response.content
        self.assertNotEqual(None, content, "Returned Json response was NONE!!")
        json_array = eval(content)
#        print 'JSON ARRAY', json_array
        self.assertNotEqual(0, len(json_array), "Returned Json list is empty!!")
        for joke in json_array:
            self.assertNotEqual('', joke['value'], "Joke value can't be empty")
            
    def test_subscribe_new_listener(self):
        response = self.client.get(reverse('eSmile.main.views.subscribe'), data = {"subscriberEmail": SUBSCRIBER_EMAIL, 'tellerUsername': TELLER_NAME})
        self.assertNotEqual(None, response, "No response returned")
        response_code = 200
        self.assertEqual(response_code, response.status_code, "Wrong Http status code returned, expected %s, found %s"% (response_code, response.status_code))
        response_content = response.content
        self.assertNotEqual(None, response_content, 'Returned response content is empty!')
        self.assertNotEqual(0, len(response_content), 'Returned response content is empty!')
#        print response.content
        json_response = eval(response_content.replace('true', 'True'))
        
        self.assertTrue(json_response.get('success') != None, "Improperly constructed json object, success field missing")
        self.assertTrue(json_response.get('success'), "Json object success field should state True, %s found!" % str(json_response['success']))
        
        
         
        #check if test teller has new subscriber
        listener_list = subscriberfacade.get_subscribers(self.teller)
        listener_found = False
        for listener in listener_list:
            if listener.username == SUBSCRIBER_EMAIL:
                listener_found = True
                
        self.assertTrue(listener_found, "New subscriber was not found in %s list"%self.teller.username)
    
    def test_add_new_joke(self):
        response = self.client.post(reverse('eSmile.jokeserver.views.add'), data = {"jokeValue": JOKE_4, 'jokeTeller': TELLER_NAME})
        self.assertNotEqual(None, response, "No response returned")
        response_code = 200
        self.assertEqual(response_code, response.status_code, "Wrong Http status code returned, expected %s, found %s"% (response_code, response.status_code))
        response_content = response.content
        self.assertNotEqual(None, response_content, 'Returned response content is empty!')
        self.assertNotEqual(0, len(response_content), 'Returned response content is empty!')
#        print response.content
        json_response = eval(response_content.replace('true', 'True'))
        
        self.assertTrue(json_response.get('success') != None, "Improperly constructed json object, success field missing")
        self.assertTrue(json_response.get('success'), "Json object success field should state True, %s found!" % str(json_response['success']))
        
        
        self.assertTrue(json_response.get('joke') != None, "Improperly constructed json object, success field missing")
        self.assertTrue(json_response.get('joke'), "Json object success field should state True, %s found!" % str(json_response['success']))
                  
        
        
        
        
        
        
        
        
        
        