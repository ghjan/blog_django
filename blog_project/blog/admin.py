# _*_ coding: utf-8 _*_

from django.contrib import admin
from blog.models import Post, Category, Tag, Author


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'modified_time', 'category', 'author']
    list_per_page = 50
    list_filter = ('author', 'category')
    search_fields = ('title',)
    date_hierarchy = 'create_time'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = "Blog Manager System"
admin.site.site_title = "Blog Manager"
