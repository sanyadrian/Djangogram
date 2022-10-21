from django.contrib import admin
from djangogram.models import Post, Profile, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['description', 'created']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'profile_image']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'posts']


admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag)
