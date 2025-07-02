from django.db import models

class TimeStampModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)  
  updated_at = models.DateTimeField(auto_now=True) 
  
  class Meta:
    abstract = True

class Image(TimeStampModel):
  image = models.ImageField()

  def __str__(self):
    return str(self.image.name)

class Function(TimeStampModel):
  function_name = models.CharField(max_length=255,null=False,blank=False)
  function = models.CharField(max_length=255,null=False,blank=False)

  def __str__(self):
    return self.function_name

class Shortcut(TimeStampModel):
  shortcut_name = models.CharField(max_length=255,null=False,blank=False)
  shortcut = models.CharField(max_length=255,null=False,blank=False)

  def __str__(self):
    return self.shortcut_name


class Category(TimeStampModel):
  category = models.CharField(max_length=255, unique=True)

  def __str__(self):
    return self.category


class Article(TimeStampModel):
  title = models.CharField(max_length=255,null=False,blank=False)
  short_desc = models.CharField(max_length=255,null=False,blank=False)
  explanation = models.TextField(null=False,blank=False)
  #relaciones
  category = models.ManyToManyField(Category)
  image = models.ManyToManyField(Image)
  function = models.ManyToManyField(Function)
  shortcut = models.ManyToManyField(Shortcut)
  
  def __str__(self):
    return self.title