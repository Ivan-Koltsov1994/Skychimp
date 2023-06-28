from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)