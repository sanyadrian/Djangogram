from django.contrib import admin
from djangogram.models import Post, Profile, Tag, PostImage


class PostImageAdmin(admin.StackedInline):
    model = PostImage


class PostAdmin(admin.ModelAdmin):
    list_display = ['description', 'created']
    inlines = [PostImageAdmin]

    class Meta:
        model = Post


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'profile_image']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'posts']


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag)
