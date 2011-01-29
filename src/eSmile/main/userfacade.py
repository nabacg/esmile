from django.contrib.auth.models import User

def get_most_active_users():
    most_active = User.objects.order_by('-last_login')[0:10]
    
    return most_active