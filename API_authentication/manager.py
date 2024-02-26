from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, username, email, password=None, password2=None, **extra_fields):
        """
            Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        username = username
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        # user.is_active = False
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        # user = self.create_user(username=username, email=email, password=password, **extra_fields)
        # user.is_admin     = True
        # user.is_active    = True
        # user.is_staff     = True
        # user.is_superuser = True
        # user.save(using=self._db)
        # return user
           
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        return self.create_user(username, email, password, **extra_fields)