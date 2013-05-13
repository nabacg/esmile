import sys
import os

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

import urllib2
from BeautifulSoup import BeautifulSoup
from crawler_settings import USERNAME, ROZRABIAKI_JOKES_URL, START_PAGE_INDEX

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
    postList = soup.find('table')
    for post in postList.findAll('tr'):
        for joke in post.findAll('td', attrs={'class':'fot'}):
            joke_text = ''
            for tag in joke.contents:
                if tag.find('<') == -1 and tag.find('>') == -1:
                    joke_text += tag.strip()
                elif tag.find('<br') != -1 or tag.find('<BR') != -1:
                    joke_text += '\n'
                    
            joke_list.append(joke_text)
                
    return joke_list

def save_joke_list(joke_list, user):
    for joke in joke_list:
        if len(user.jokes.filter(value = joke)) == 0:
            print "Adding new joke"
            user.jokes.create(value = joke)                
        else:
            print "We already had this one"    

def import_latest_jokes():
    page_num = START_PAGE_INDEX
    url = ROZRABIAKI_JOKES_URL 
    while(page_num >= 0):
        user = User.objects.get(username = USERNAME)
        save_joke_list(get_joke_list(read_page(url%page_num)), user)
        page_num -= 1    

def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    import_latest_jokes()
    


if __name__ == '__main__':
    main()
