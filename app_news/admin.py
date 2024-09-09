from django.contrib import admin
from .models import News, Categories, Authors, Contact

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'category', 'published_time', 'status']
    list_filter = ['category', 'status', 'created_time']
    prepopulated_fields = {'slug': ('title',)}


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