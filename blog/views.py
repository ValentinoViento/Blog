from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog
from django.contrib.auth.forms import UserCreationForm
from django import forms
from ckeditor.widgets import CKEditorWidget # type: ignore
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

    def form_valid(self, form):
        form.instance.autor = self.request.user  # Asignar el usuario actual como autor
        return super().form_valid(form)



    # def get_form(self):
    #     form = super().get_form()
    #     form.fields['texto'].widget = CKEditorWidget()
    #     return form


class VerBlog(ListView):
    model = Blog
    template_name = 'ver_blog.html'

    def get_queryset(self):
        return Blog.objects.all()


class MisPosts(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'mis_posts.html'

    def get_queryset(self):
        return Blog.objects.filter(autor=self.request.user)

    def post(self, request):
        seleccion = request.POST.getlist('seleccion')
        
        if request.POST.get("confirmar_eliminacion"):   # Verifica si se selecciona el boton para eliminar
            Blog.objects.filter(pk__in=seleccion, autor=self.request.user).delete()     #utiliza pk para eliminar los seleccionados por el usuario
            return redirect('mis_posts') 

        else:
            # Obtener los objetos Blog correspondientes a los IDs seleccionados
            posts_seleccion = Blog.objects.filter(pk__in=seleccion)
            return render(request, 'confirmar_eliminacion.html', {'posts_seleccion': posts_seleccion})
    


#https://www.youtube.com/watch?v=zeoT66v4EHg

def home_view(request):
    return render(request, 'home.html')