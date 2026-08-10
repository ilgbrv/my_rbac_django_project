import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

class CustomJWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        
        auth_header = request.headers.get('Authorization')
        request.user = AnonymousUser()

        if auth_header:
            try:
                auth_type, token = auth_header.split(' ')
                
                if auth_type.lower() == 'bearer':
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                    
                    user_id = payload.get('user_id')
                    
                    if user_id:
                        user = User.objects.get(id=user_id)
                        
                        if user.is_active:
                            request.user = user
                            
            except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist, ValueError):
                pass

        response = self.get_response(request)
        return response