from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog
from django.contrib.auth.forms import UserCreationForm
from django import forms
from ckeditor.widgets import CKEditorWidget
# Create your views here.

class RegistroUsuario(CreateView):
    template_name = 'registration/registro.html'   #por defecto se deja en template y se llama de manera normal, por separarlo y unificar el login/registro, lo modifico a la ruta "/registration" y lo llamo la ruta de esta manera
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['titulo', 'texto']

class CrearPost(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'crear_post.html'
    success_url = reverse_lazy('mis_posts')

    def get_form(self):
        form = super().get_form()
        form.fields['texto'].widget = CKEditorWidget()
        return form


class VerBlog(ListView):
    model = Blog
    template_name = 'ver_blog.html'

    def get_queryset(self):
        return Blog.objects.all()


class MisPosts(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'mis_posts.html'

    def get_queryset(self):
        return Blog.objects.filter(autor=self.request.user) #filtra por los objetos propios de cada usuario
    
    def post(self, request):
        seleccion = request.POST.getlist('seleccion')   #selecciona mediante id
        Blog.objects.filter(pk__in=seleccion, autor=request.user).delete()      #borra los seleccionados, siendo post propios de el usuario
        return redirect('mis_posts')    #redirige y se queda con sus posts sin eliminar
    
    
class EliminarPosts(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'confirmar_eliminacion.html'
    success_url = reverse_lazy('mis_posts')

    def get_object(self, queryset=None):
        return get_object_or_404(Blog, pk=self.kwargs['pk'], autor=self.request.user) #si encuentra el objeto, consigue su "pk" para decidir eliminarlo
    
    #def get_queryset(self):
    #     return Blog.objects.filter(autor=self.request.user)



def home_view(request):
    return render(request, 'home.html')