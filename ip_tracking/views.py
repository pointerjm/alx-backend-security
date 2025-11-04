from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', block=True)
def anonymous_view(request):
    return JsonResponse({"message": "Anonymous request accepted"})

@ratelimit(key='ip', rate='10/m', block=True)
@login_required
def authenticated_view(request):
    return JsonResponse({"message": "Authenticated request accepted"})
