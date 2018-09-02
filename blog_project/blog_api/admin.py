from django.contrib import admin

from blog_api.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'excerpt', 'create_time', 'modified_time']
    list_per_page = 50
    search_fields = ('title', 'body',)
    date_hierarchy = 'create_time'
