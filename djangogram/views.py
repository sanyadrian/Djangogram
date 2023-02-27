from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from djangogram.models import (
    Post, Profile, Tag, User, Like, PostImage, UserFollowing
)
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, resolve
from djangogram.forms import (
    NewUserForm, ProfileForm, UserForm, PostForm, PostImageForm
)
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from djangogram.tokens import account_activation_token
from djangogram.utils import extract_tags
from django.db import transaction


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
    # post = get_object_or_404(Post, pk=pk)
    post = get_object_or_404(Post, pk=pk)
    photos = PostImage.objects.filter(post=post)
    # total_likes = Like.objects.filter(post__author=post.author).count()
    total_likes = post.post_likes.count()
    context = {
        'post': post,
        'total_likes': total_likes,
        'photos': photos,
    }
    return render(request, 'djangogram/post.html', context)


# def post(request, pk, tag):
#     # post = Post.objects.get(pk=pk)
#     # post = get_object_or_404(Post, pk=pk)
#     # tag = request.GET.get('tag')
#     post = get_object_or_404(Post, pk=pk)
#     photos = PostImage.objects.filter(post=post)
#     tags = get_object_or_404(Tag, tag=tag)
#     # total_likes = Like.objects.filter(post__author=post.author).count()
#     total_likes = post.post_likes.count()
#     context = {
#         'post': post,
#         'total_likes': total_likes,
#         'photos': photos,
#         'tags': tags
#     }
#     return render(request, 'djangogram/post.html', context)


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


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request, 'Thank you for your email confirmation.'
                     ' Now you can login your accout'
        )
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid')
    return redirect('profiles')


def activateEmail(request, user, to_email):
    mail_sibject = "Activate your user account"
    message = render_to_string(
        "djangogram/template_activate_account.html", {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }
    )
    email = EmailMessage(mail_sibject, message, to=[to_email])
    if email.send():
        messages.success(request, 'Registration succesful')
    else:
        messages.error(
            request, "Unsuccessful registration. Invalid information"
        )


def register_request(request):
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        form = NewUserForm(request.POST)
        # form_user = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_activate = False
            user.save()
            Profile.objects.create(user=user, bio='1')
            # form_user.save()
            # login(request, user)

            # messages.success(request, 'Registration succesful')
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('profiles')
        messages.error(
            request, "Unsuccessful registration. Invalid information"
        )
    form = NewUserForm()
    # form_user = ProfileForm()
    return render(
        request=request,
        template_name='djangogram/register.html',
        context={
            'register_form': form,
            # 'form_user': form_user
        }
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


# @login_required(login_url='login')
# def create_post(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(
#             request.POST, request.FILES
#         )
#         form_image = PostImageForm(
#             request.POST, request.FILES
#         )
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.author = request.user.profile
#             instance.save()
#             extract_tags(instance)
#             return redirect('profile', pk=request.user.profile.id)
#     context = {
#         'form': form,
#     }
#     return render(request, 'djangogram/create_post.html', context)


@login_required(login_url='login')
def create_post(request):
    form = PostForm()
    form_image = PostImageForm()
    if request.method == 'POST':
        form = PostForm(
            request.POST, request.FILES
        )
        form_image = PostImageForm(
            request.POST, request.FILES
        )
        if form.is_valid() and form_image.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user.profile
            # instance_image.post.author = request.user.profile
            instance.save()
            for file in request.FILES.getlist('images'):
            #     instance_image = form_image.save(commit=False)
            #     instance_image.post = instance
            #     instance_image.image = file
            #     instance_image.save()
                PostImage.objects.create(post=instance, image=file)
            extract_tags(instance)
            return redirect('profile', pk=request.user.profile.id)
    context = {
        'form': form,
        'form_image': form_image
    }
    return render(request, 'djangogram/create_post.html', context)


def post_by_tags(request):
    tag = request.GET.get('tag')
    obj, _ = Tag.objects.get_or_create(name=tag)
    context = {
        'posts': obj.posts.all()
    }
    return render(request, 'djangogram/tag.html', context)


def follow(request):
    username = request.POST.get('username')
    user = request.user
    # import ipdb; ipdb.set_trace()
    following = get_object_or_404(User, username=username)
    new_follower = UserFollowing.objects.filter(user=user, following_user=following)
    # import ipdb; ipdb.set_trace()
    if new_follower.exists():
        new_follower.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    UserFollowing.objects.create(user=user, following_user=following)
    # return HttpResponseRedirect(
    #     reverse('profile', kwargs={'pk': following.profile.id})
    # )
    return redirect(request.META.get('HTTP_REFERER'))