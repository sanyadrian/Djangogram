# from djangogram.models import Profile
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.contrib.auth.models import User
#
#
# def update_user(sender, instance, created, **kwargs):
#     profile = instance
#     user = profile.user
#     if not created:
#         user.first_name = profile.user.first_name
#         user.username = profile.user.username
#         user.email = profile.user.email
#         user.save()
#
#
# post_save.connect(update_user, sender=Profile)