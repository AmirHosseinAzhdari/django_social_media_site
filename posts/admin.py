from django.contrib import admin
from .models import Post


# customize admin panel
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'updated', 'created')
    search_fields = ('slug', 'body')
    list_filter = ('updated', 'created')
    # complete slug when typing body
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)


# admin.site.register(Post, PostAdmin)
