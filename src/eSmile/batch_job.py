#! /usr/bin/env python

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

def main(argv=None):
    if argv is None:
        argv = sys.argv

    for joke in Joke.objects.all():
        joke.value = joke.value.replace('<br/>', '\n')
        joke.save()
#
#    joke = Joke.objects.all()[0]
#    message = joke.value
#    
#
#    send_mail('Admin\'s last Joke',
#              message,
#              'nabacg@gmail.com',
#              ['grigoriij@o2.pl', 
#               'gmdc.inc@gmail.com'])

if __name__ == '__main__':
    main()