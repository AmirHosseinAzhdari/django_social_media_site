from django.contrib import admin
from .models import Post, Comment


# customize admin panel
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'updated', 'created')
    search_fields = ('title', 'body')
    list_filter = ('updated', 'created')
    # complete slug when typing body
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'is_reply', 'created')
    raw_id_fields = ('user', 'post', 'reply')
