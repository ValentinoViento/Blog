from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify


class Blog(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    texto = CKEditor5Field('Texto', config_name ='extends', blank=True)
    fechaCreado = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super(Blog, self).save(*args, **kwargs) 
    

    def __str__(self):
        return self.titulo
    