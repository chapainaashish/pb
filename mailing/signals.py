from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactEntry, Subscriber
from base import config


@receiver(post_save, sender=Subscriber)
def from_user(sender, instance, **kwargs):
    # Email sent to admin
    send_mail("Subscriber",
              "From: " + instance.name + "\nEmail: " + instance.email + "\nCountry: " + instance.country,
              '',
              [config.DEFAULT_TO_EMAIL])


@receiver(post_save, sender=Subscriber)
def from_admin(sender, instance, **kwargs):
    # Email sent to user
    send_mail("Confirmation Subscription",
              "Thanks for subscribing to our newsletter!",
              '',
              [instance.email])
