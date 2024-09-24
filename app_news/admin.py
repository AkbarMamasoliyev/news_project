from django.contrib import admin
from .models import News, Categories, Authors, Contact, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'category', 'published_time', 'status']
    list_filter = ['category', 'status', 'created_time']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['body']


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Authors)
class AuthorsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['body', 'user', 'created_time', 'active']
    list_filter = ['user', 'created_time', 'active']
    search_fields = ['body', 'user__username']
    actions = ['disable_comments', 'activate_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)
