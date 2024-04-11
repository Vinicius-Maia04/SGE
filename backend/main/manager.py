from django.contrib.auth.models import BaseUserManager
import random

class CustomManager(BaseUserManager):

    def create_user(self, email, password, registrationNumber=None, **extra_fields):

        if not email:
            raise  ValueError("Invalid e-mail!")
        if not password:
            raise  ValueError("Invalid password!")
        
        regNumber = registrationNumber

        if not regNumber:
            regNumber = random.randint(1,100000)

        email = self.normalize_email(email)
        active = extra_fields.get('is_active')
        if not active:
            active = True

        user = self.model(
            email=email,            
            is_active=active,
            is_staff=active,
            registrationNumber=regNumber,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, email, password, **extra_fields):

        user = self.create_user(
            email=email,
            password=password,                     
            **extra_fields
        )
        user.is_superuser = True

        user.save()
        return user
            
        