from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.postgres.search import SearchVector

from blog.forms import SearchForm
from blog.models import Post
from blog.services import send_post_email


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    extra_context = {
        'message_list': Post.objects.all(),
        'title': 'Лист блоговой информации'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published=True)
        if self.request.user.has_perm('blog.can_change_post'):
            return queryset
        return queryset


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.view_count += 1
        if obj.view_count == 100:
            send_post_email(obj)
        obj.save()
        return obj


class PostCreateView(CreateView):
    model = Post

    fields = ('name', 'content', 'image', 'published')
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    model = Post

    fields = ('name', 'content', 'image', 'published')
    success_url = reverse_lazy('blog:post_list')

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    model = Post
    fields = ('name', 'content', 'image', 'published')

    def get_success_url(self):
        return reverse('blog:post_item', args=[str(self.object.slug)])


def toggle_publish(request, slug):
    """Функция перезаполнения поста"""
    post_item = get_object_or_404(Post, slug=slug)
    if post_item.published:
        post_item.published = False
    else:
        post_item.published = True

    post_item.save()

    return redirect(reverse('blog:blog_item', args=[post_item.slug]))


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('name', 'content'),
            ).filter(search=query)
    return render(request,
                  'blog/blog/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
