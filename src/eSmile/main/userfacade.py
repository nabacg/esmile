from django.contrib.auth.models import User
from django.db.models import Count

def get_most_active_users():
   # most_active = User.objects.order_by('-last_login')[0:10]
    most_active = User.objects.annotate(num_of_jokes = Count('jokes')).order_by('-num_of_jokes')[0:10]
    return most_active