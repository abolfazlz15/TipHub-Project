from videos.models import Category , Notification
from django.contrib.auth.decorators import login_required


def categories(request):
    category = Category.objects.filter(parent=None)
    return {'categories': category}



def notifications(request): # This section has not been completed.
    if request.user.is_authenticated:
        notification =  Notification.objects.all().order_by('-id')
    notification =  Notification.objects.all().order_by('-id')

    return {'notifications': notification}