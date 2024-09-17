from pyexpat.errors import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog
from django.contrib.auth.forms import UserCreationForm
from django import forms


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
        form.instance.autor = self.request.user  # asigna el usuario actual como autor
        return super().form_valid(form)
    


class VerBlog(ListView):
    model = Blog
    template_name = 'ver_blog.html'

    def get_queryset(self):
        return Blog.objects.all()           #para ver a todos los usuarios y sus posts


class MisPosts(LoginRequiredMixin, ListView, DeleteView):
    model = Blog
    template_name = 'mis_posts.html'

    def get_queryset(self):
        return Blog.objects.filter(autor=self.request.user)

    def post(self, request):
        if request.method == 'POST':
            seleccion = request.POST.getlist('seleccion')
            if request.POST.get("confirmar_eliminacion"):
                posts_seleccion = Blog.objects.filter(pk__in=seleccion, autor=self.request.user)    #Selección de posts
                posts_seleccion.delete()            # Eliminar los posts seleccionados
                messages.success(request, 'Posts eliminados exitosamente.')
                return redirect('mis_posts')
            else:
                posts_seleccion = Blog.objects.filter(pk__in=seleccion, autor=self.request.user)
                return render(request, 'confirmar_eliminacion.html', {'posts_seleccion': posts_seleccion})
    


def home_view(request):
    return render(request, 'home.html')