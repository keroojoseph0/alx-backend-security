from django.shortcuts import render
from django.http import JsonResponse
from ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', block=False)   # anonymous
@ratelimit(key='ip', rate='10/m', block=False)  # authenticated
def login_view(request):

    if getattr(request, 'limited', False):
        return JsonResponse(
            {"detail": "Too many requests. Please try again later."},
            status=429
        )

    return JsonResponse({"detail": "Login endpoint"})
