from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from djangogram.models import Profile, Post, PostImage


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_image')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('description',)


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)
