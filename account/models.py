import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import (
    UserManager
)
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    username = models.CharField(_("username"),max_length=256)
    user_uid = models.UUIDField(_("uuid"),default=uuid.uuid4, editable=False, blank=True)
    email = models.EmailField(_("email_address"),unique=True)
    first_name = models.CharField(_("first_name"),max_length=200,default = "")
    last_name = models.CharField(_("last_name"),max_length=200,default = "")
    phone = models.CharField(_("phone"),max_length=50,default="",unique=True)
    created_at = models.DateTimeField(_("created_at"),auto_now_add=True,null=True)
    updated_at = models.DateTimeField(_("updated_at"),auto_now=True,null=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    objects = UserManager()


    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return self.username
    