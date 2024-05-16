from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) == 2 and auth_header[0].lower() == 'token':
            try:
                token = Token.objects.get(key=auth_header[1])
                request.user = token.user
            except Token.DoesNotExist:
                request.user = AnonymousUser()

        response = self.get_response(request)
        return response