from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('news', views.news, name='news'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('register', views.registerPage, name='register'),
    path('upload/', views.upload, name='upload-post'),
    path('update/<int:post_id>', views.update_post),
    path('delete/<int:post_id>', views.delete_post)

]
