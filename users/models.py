import bcrypt
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True) 
    def __str__(self):
        return self.role_name
    
class AccessRoleRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='rules')
    element_name = models.CharField(max_length=100)

    read_permission = models.BooleanField(default=False)  
    create_permission = models.BooleanField(default=False) 
    update_permission = models.BooleanField(default=False) 
    delete_permission = models.BooleanField(default=False) 

    read_all_permission = models.BooleanField(default=False)   
    update_all_permission = models.BooleanField(default=False) 
    delete_all_permission = models.BooleanField(default=False) 

    def __str__(self):
        return f"Правила роли {self.role.role_name} для сущности {self.element_name}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен для заполнения')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150, blank=True, null=True)

    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['first_name', 'last_name'] 

    def set_password(self, raw_password):
        password_bytes = raw_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        self.password = hashed_password.decode('utf-8')

    def check_password(self, raw_password):
        password_bytes = raw_password.encode('utf-8')
        hashed_bytes = self.password.encode('utf-8')   
        return bcrypt.checkpw(password_bytes, hashed_bytes) 


    def __str__(self):
        return self.email
