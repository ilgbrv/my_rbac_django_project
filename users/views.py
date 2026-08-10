import jwt
import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer
from .permission import CustomRBACPermission

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Вы успешно зарегистрированы!"}, 
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email и пароль обязательны"}, status=400)

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response({"error": "Неверный email или пароль"}, status=401)

        if not user.is_active:
            return Response({"error": "Учетная запись деактивирована"}, status=403)

        if not user.check_password(password):
            return Response({"error": "Неверный email или пароль"}, status=401)

        payload = {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),  
            "iat": datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({"access_token": token}, status=200)


        
class DeleteAccountView(APIView):
    def delete(self, request):
        user = request.user

        if not user or not user.is_authenticated:
            return Response({"detail": "Учетные данные не предоставлены."}, status=401)

        user.is_active = False
        user.save()

        return Response(
            {"detail": "Аккаунт успешно деактивирован. Сессия завершена."}, 
            status=200
        )
    
class MockProjectListView(APIView):
    permission_classes = [CustomRBACPermission]
    
    required_element = 'projects'


    def get(self, request):
        mock_projects = [
            {"id": 1, "title": "Разработка секретного бэкенда", "status": "В процессе"},
            {"id": 2, "title": "Сдача ТЗ на отлично", "status": "Выполнено"}
        ]
        return Response(mock_projects, status=200)