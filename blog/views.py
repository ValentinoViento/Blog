from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.messages import success
from django_ckeditor_5.widgets import CKEditor5Widget


# Create your views here.

class RegistroUsuario(CreateView):
    template_name = 'registration/registro.html'   #por defecto se deja en template y se llama de manera normal, por separarlo y unificar el login/registro, lo modifico a la ruta "/registration" y lo llamo la ruta de esta manera
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class BlogForm(forms.ModelForm):
    class Meta:
          model = Blog
          fields = ("titulo", "texto")
          widgets = {
              "texto": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="texto"
              )
          }
        
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
    paginate_by = 5

    def get_queryset(self):
        return Blog.objects.all().order_by('-fechaCreado')            #para ver a todos los usuarios y sus posts


class BlogContenido(DetailView):
    model = Blog
    template_name = 'blog_contenido.html'          #para poder entrar a cada post y ver su contenido




class MisPosts(LoginRequiredMixin, View):
    template_name = 'mis_posts.html'

    def get(self, request):
        posts = Blog.objects.filter(autor=request.user)
        return render(request, self.template_name, {'object_list': posts})

    def post(self, request):
        seleccion = request.POST.getlist('seleccion')
        if request.POST.get("confirmar_eliminacion"):
            # Eliminar los posts seleccionados
            Blog.objects.filter(pk__in=seleccion, autor=request.user).delete()
            success(request, 'Posts eliminados exitosamente.')  # Add success message
            return redirect('mis_posts')
        else:
            # Mostrar la página de confirmación
            posts_seleccion = Blog.objects.filter(pk__in=seleccion, autor=request.user)
            return render(request, 'confirmar_eliminacion.html', {'posts_seleccion': posts_seleccion})






def home_view(request):
    return render(request, 'home.html')