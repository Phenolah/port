from django.contrib.auth.models import User

def portfolio_context(request):
    context = {
        'me': User.objects.first(),
    }
    return context
