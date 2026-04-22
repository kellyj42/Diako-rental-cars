# userAuth/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from allauth.socialaccount.signals import social_account_added
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(email_confirmed)
def mark_profile_verified_on_email_confirmation(request, email_address, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=email_address.user)
    if not profile.is_verified:
        profile.is_verified = True
        profile.save(update_fields=["is_verified"])


@receiver(social_account_added)
def mark_profile_verified_on_social_connect(request, sociallogin, **kwargs):
    user = sociallogin.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if EmailAddress.objects.filter(user=user, verified=True).exists() and not profile.is_verified:
        profile.is_verified = True
        profile.save(update_fields=["is_verified"])
