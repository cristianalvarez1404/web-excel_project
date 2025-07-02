from django.db import models
from django.contrib.auth.models import AbstractUser

class TypeUser(models.Model):
  type = models.CharField(max_length=255,null=False,blank=False)
  created_at = models.DateTimeField(auto_now_add=True)  
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.type

class CustomUser(AbstractUser):
  phone = models.CharField(max_length=255,null=True,blank=True)
  address = models.CharField(max_length=255,null=True,blank=True)
  type_user = models.ForeignKey(TypeUser,on_delete=models.SET_NULL,null=True)
  
  def __str__(self):
    return self.username
