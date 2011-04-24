import urllib2
from BeautifulSoup import BeautifulSoup
import sys
import os
from crawler_settings import USERNAME, GL_TOP_JOKES_URL

def setup_environment():
    pathname = os.path.dirname(sys.argv[0])
    sys.path.append(os.path.abspath(pathname))
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Must set up environment before imports.
setup_environment()

from django.core.mail import send_mail
from django.contrib.auth.models import User
from jokeserver.models import Joke
from jokeserver import notificationfacade

def read_page(url):
    content = "EMPTY"
    try:
        print "Reading " + url
        response = urllib2.urlopen(url)
        content = response.read()
    except IOError, e:
        if hasattr(e, 'code'):
            if e.code == 401:
                print e.code, e
            elif e.code == 404:
                print e
                #read_page(url, page_number -1)
            else:
                print e.headers
                print e.headers.get('www-authenticate')
        return False
    
    

    return content

def get_joke_list(page_content):
    joke_list = []
    soup = BeautifulSoup(page_content)
    postList = soup.find('div', attrs={'id':'postsList'})
    for post in postList.findAll('div'):
        for body in post.findAll('div', attrs={'class':'body'}):
            for joke in body.findAll('div', attrs={'class':'cloud'}):            
               
                joke_text = ''
                for tag in joke.contents:
                    if tag.find('<') == -1 and tag.find('>') == -1:
                        joke_text += tag.strip()
                    elif tag.find('<br') != -1 or tag.find('<BR') != -1:
                        joke_text += '\n'
                joke_list.append(joke_text)
                
    return joke_list

#import os.path
if os.name == 'nt':
    pickle_file = 'last_page_number.txt'
else:
    picke_file = '/home/gmc/www/eSmile/eSmileRepo/eSmile/src/eSmile/JokeSpider/last_page_number.txt'

def get_page_number():
    f = open(pickle_file, 'r')
    num = int(f.read())
    
    return num

def set_page_number(page_number):
    f = open(pickle_file, 'w')
    f.write(str(page_number))

def save_joke_list(user, joke_list):
    for joke in joke_list:
        if len(user.jokes.filter(value = joke)) == 0:
            print "Adding new joke"
                #Joke.objects.create(owner=user, value = joke)
            user.jokes.create(value = joke)
        else:
            print "We already had this one"    

#! /usr/bin/env python
top_kawaly_last_page = GL_TOP_JOKES_URL#'http://www.goldenline.pl/forum/143463/top-kawaly/s/%i'
username = USERNAME #'admin'


def import_GL_top_jokes():
    last_visited_page_num = get_page_number()
    user = User.objects.get(username = username)

##czyli to jest totalnie do dupy bo GL zawsze przekieruje na ostatnia strone nawet
##jak podamy numer z poza zakresu
    prev_first_joke = ''
    page_content = read_page(top_kawaly_last_page%last_visited_page_num)
    joke_list = get_joke_list(page_content)    

    while prev_first_joke != joke_list[-1]:
        save_joke_list(user, joke_list)

        prev_first_joke = joke_list[-1]
        last_visited_page_num += 1
        page_content = read_page(top_kawaly_last_page%last_visited_page_num)
        joke_list = get_joke_list(page_content)

    set_page_number(last_visited_page_num)
    
def main(argv=None):
    if argv is None:
        argv = sys.argv
    #print get_joke_list(read_page(top_kawaly_last_page))
    import_GL_top_jokes()

if __name__ == '__main__':
#    print read_page('http://www.goldenline.pl')
#    print read_page(top_kawaly_last_page)
    main()
