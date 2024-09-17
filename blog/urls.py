from django.urls import path
from blog import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('blog/', views.VerBlog.as_view(), name='ver_blog'),
    path('crear/', views.CrearPost.as_view(), name='crear_post'), 
    path('mis_posts/', views.MisPosts.as_view(), name='mis_posts'),
]
