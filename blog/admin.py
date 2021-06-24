from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . models import *
# Register your models here.


# admin.site.register(Author)

# admin.site.register(Category)

# admin.site.register(Tag)

# admin.site.register(Post)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('email')
    fields = ['email']
    search_fields = ['name','email']
    ordering = ['name']
    list_filter = ['active','created_on']
    date_hierarchy = 'created_on'

class PostAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['title']}),
    (None, {'fields':['author']}),
    (None, {'fields':['category']}),
    (None, {'fields':['content']}),
    ('Tags', {'fields':['tags'], 'classes':['collapse']}),
    (None, {'fields':['slug']})]
    list_display = ('title', 'author', 'category')
    list_filter = ['pub_date',]
    search_fields = ['title', 'author', 'tags',]
    ordering = ['-pub_date']
    # filter_horizontal = ['tags']
    raw_id_fields = ['tags',]
    readonly_fields = ('slug',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',) 
    readonly_fields = ('slug',)  


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    readonly_fields = ('slug',)

class FeedbackAdmin(admin.ModelAdmin):
    list_display= ('name', 'email','date','subject',)
    search_fields = ('name','email',)
    date_hierarchy = 'date'

admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Feedback,FeedbackAdmin)

