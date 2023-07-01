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
from django.contrib.auth.decorators import login_required
from django.urls import path

from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, toggle_publish
from django.views.decorators.cache import never_cache, cache_page
app_name = BlogConfig.name

urlpatterns = [
    path('blog/', cache_page(60)(PostListView.as_view()), name='post_list'),
    path('blog/<slug:slug>/', never_cache(PostDetailView.as_view()), name='post_item'),
    path('create/', never_cache(PostCreateView.as_view()), name='post_create'),
    path('blog/update/<slug:slug>/', never_cache(PostUpdateView.as_view()), name='post_update'),
    path('blog/delete/<slug:slug>/', never_cache(PostDeleteView.as_view()), name='post_delete'),
    path('blog/toggle/<slug:slug>/', login_required(toggle_publish), name='toggle_publish')

]