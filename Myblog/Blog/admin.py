from django.contrib import admin
from .models import Post, Comment, Review
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'slug', 'status', 'created_on')
    list_filter = ("status",'category')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)



class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text', 'rate', 'date')
    list_filter = ('post', 'rate')
    search_fields = ('post','rate')

admin.site.register(Review, ReviewAdmin)