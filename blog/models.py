from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify


class Blog(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)                    #utilización de slug para identificar de manera única cada post. Ideal para el uso de Blogs(en este caso, esencial)
    texto = models.CharField(max_length=1000, db_index=True, unique=True, blank=True)  # usar TextField si necesito más texto
    fechaCreado = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):                    #función para establecer un slug, en caso de no haberse creado previamente de manera manual
        if not self.slug:
            self.slug = slugify(self.titulo)                #slugify, función para crear un slug tomando cómo referencia (en este caso, el título) y creando una cadena de caracteres ASCII en minúscula y guiones (-)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class Comentarios(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='comentarios')              #blog obligatorio, para poder identificar cada post y los comentarios en los correspondientes
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = CKEditor5Field('Comentario', config_name='coment', blank=True)
    fechaCreado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor} commented on {self.blog.titulo}"
    
