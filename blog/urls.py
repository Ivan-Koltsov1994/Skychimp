"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, toggle_publish
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', PostListView.as_view(), name='post_list'),
    path('blog/<slug:slug>/', PostDetailView.as_view(), name='post_item'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('blog/update/<slug:slug>/', PostUpdateView.as_view(), name='post_update'),
    path('blog/delete/<slug:slug>/', PostDeleteView.as_view(), name='post_delete'),
    path('blog/toggle/<slug:slug>/', toggle_publish, name='toggle_publish')

]