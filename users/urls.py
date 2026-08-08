from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, DeleteAccountView, MockProjectListView 

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    path('projects/', MockProjectListView.as_view(), name='project_list'),
]

