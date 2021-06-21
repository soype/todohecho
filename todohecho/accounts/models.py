from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django.db.models.signals import pre_save


# Create your models here.

def get_profile_image_filepath(self,filename):
    return f"profile_images/{self.pk}/{'profile_image.png'}"
    

def get_default_profile_image():
    return 'profile_images/logo_1080.png'
    # return 'accounts/static/accounts/logo_1080.png'

class MyAccountManager(BaseUserManager):

    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Se debe registrar un mail válido")
        if not username:
            raise ValueError("Por favor, ingresá un nombre de usuario")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password=password
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email           = models.EmailField(verbose_name="Email",max_length=60,unique=True)
    username        = models.CharField(verbose_name="Usuario",max_length=30, unique=True)
    date_joined     = models.DateTimeField(verbose_name="Fecha en que se unió", auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name="Última sesión", auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    profile_image   = models.ImageField(max_length=255, upload_to=get_profile_image_filepath,null=True,blank=True,default=get_default_profile_image)
    first_name      = models.CharField(verbose_name="Nombre", max_length=60)
    last_name       = models.CharField(verbose_name="Apellido", max_length=60)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self) -> str:
        return self.username
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def get_absolute_url(self):
        return reverse('accounts:account', kwargs={'pk':self.pk})

    def has_module_perms(self,app_label):
        return True
    
    def delete_image(self):
        self.profile_image.delete()
        self.save()
