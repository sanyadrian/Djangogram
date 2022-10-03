from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Profile, Tag, User, Like
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'djangogram/profiles.html', context)


def profile(request, pk):
    profile = get_object_or_404(Profile.objects.select_related('user'), pk=pk)
    context = {'profile': profile}
    return render(request, 'djangogram/profile.html', context)


def post(request, pk):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post}
    return render(request, 'djangogram/post.html', context)


def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    context = {'tag': tag}
    return render(request, 'djangogram/tag.html', context)


@csrf_exempt
def like(request):
    user_id = request.user.id
    post_id = request.POST.get('post_id')
    Like.objects.create(user_id=user_id, post_id=post_id)
    return HttpResponse(201)

