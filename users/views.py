from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .permission import CustomRBACPermission


from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Вы успешно зарегистрированы!"}, 
            status=status.HTTP_201_CREATED
        )

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()

        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  
        except Exception:
            pass
            
        return Response(
            {"detail": "Аккаунт успешно деактивирован. Сессия завершена."}, 
            status=200
        )
    
class MockProjectListView(APIView):
    permission_classes = [CustomRBACPermission]
    
    required_resource = 'Projects'
    required_action = 'view'

    def get(self, request):
        mock_projects = [
            {"id": 1, "title": "Разработка секретного бэкенда", "status": "В процессе"},
            {"id": 2, "title": "Сдача ТЗ на отлично", "status": "Выполнено"}
        ]
        return Response(mock_projects, status=200)