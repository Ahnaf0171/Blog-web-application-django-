from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
   
    path('',views.post_list, name="post_list"),
    path('post_details/<int:id>',views.post_details, name="post_details"),
    path('post/<int:id>/like',views.like_post, name= "like_post"),
    path('signup/', views.user_sign_up, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name = 'blog/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create_post/', views.create_post, name="create_post"),
    path('update_post/<int:id>',views.update_post,name="update_post"),
    path('delete_post/<int:id>', views.delete_post, name="delete_post")
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)