from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from djangogram.models import Post, Profile, Tag, User, Like
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, resolve
from djangogram.forms import NewUserForm, ProfileForm, UserForm, PostForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect



def profiles(request):
    posts = Post.objects.select_related('author').all().annotate(
        count=Count('post_likes')
    )
    context = {
        'posts': posts,
    }
    return render(request, 'djangogram/profiles.html', context)


def profile(request, pk):
    profile = get_object_or_404(Profile.objects.select_related('user'), pk=pk)
    posts = Post.objects.filter(
        author=profile).annotate(count=Count('post_likes')
                                 )
    context = {
        'profile': profile,
        'posts': posts

    }
    return render(request, 'djangogram/profile.html', context)


def post(request, pk):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    # total_likes = Like.objects.filter(post__author=post.author).count()
    total_likes = post.post_likes.count()
    context = {
        'post': post,
        'total_likes': total_likes
    }
    return render(request, 'djangogram/post.html', context)


@csrf_exempt
def like(request):
    user_id = request.user.id
    post_id = request.POST.get('post_id')
    new_like = Like.objects.filter(user_id=user_id, post_id=post_id)
    # import ipdb; ipdb.set_trace()
    if new_like.exists():
        new_like.delete()
        return redirect(request.META.get('HTTP_REFERER'))
        # return HttpResponseRedirect(request.path_info)
    Like.objects.create(user_id=user_id, post_id=post_id)
    return redirect(request.META.get('HTTP_REFERER'))



def register_request(request):
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration succesful')
            return redirect('profiles')
        messages.error(
            request, "Unsuccessful registration. Invalid information"
        )
    form = NewUserForm()
    return render(
        request=request,
        template_name='djangogram/register.html',
        context={'register_form': form}
    )


def loginPage(request):
    # import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # import ipdb; ipdb.set_trace()
        try:
            user = User.objects.get(username=username)
        except:
            return redirect('login')
        authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('profiles')
    # if request.user.is_authenticated:
    #     return redirect('profiles')
    return render(request, 'djangogram/login.html')


def logout_profile(request):
    logout(request)
    request.session.flush()
    request.user = AnonymousUser
    return redirect('login')


@login_required(login_url='login')
def editProfile(request):
    if not hasattr(request.user, 'profile'):
        logout(request)
        return redirect('login')
    profile = request.user.profile
    form = ProfileForm()
    form_user = UserForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        form_user = UserForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid() and form_user.is_valid():
            form.save()
            form_user.save()
            return redirect('profiles')
    context = {
        'form': form,
        'form_user': form_user
    }
    return render(request, 'djangogram/profiles_form.html', context)


@login_required(login_url='login')
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(
            request.POST, request.FILES
        )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user.profile
            instance.save()
            return redirect('profile', pk=request.user.profile.id)
    context = {
        'form': form,
    }
    return render(request, 'djangogram/create_post.html', context)


