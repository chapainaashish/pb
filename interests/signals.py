from base import config
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from .models import ReviewAndRating, Comment, Interest
import datetime


@receiver(post_save, sender=Interest)
def from_user_interest(sender, instance, **kwargs):
    if instance.display is False and instance.send_email is True:
        subject = config.INTEREST + "from User"
        body = instance.name + '\n\n' + instance.user.username + '\n\n' + instance.email1
        # Email sent to admin
        send_mail(subject,
                body,
                '',
                [config.DEFAULT_TO_EMAIL])


@receiver(post_save, sender=Interest)
def from_admin_interest(sender, instance, **kwargs):
    if instance.display is True and instance.send_email is True:
        domain = Site.objects.get_current().domain
        path = instance.get_absolute_url()  # link to the interest (for example : <interests>/france/bordeaux/<interest>/chateau-monlot/)

        subject = "Your " + config.INTEREST.lower() + " is now live"
        body = domain + path
        # Email sent to user
        send_mail(subject,
                body,
                '',
                [instance.email1])

    elif instance.display is False and instance.send_email is True:
        subject = "Thank you for your submitting the " + config.INTEREST.lower()
        body = "Admin will first review your " + config.INTEREST.lower() + " before it is displayed"
        # Email sent to user
        send_mail(subject,
                body,
                '',
                [instance.email1])


@receiver(post_save, sender=ReviewAndRating)
def from_admin_rr(sender, instance, **kwargs):
    if instance.approved is True:
        domain = Site.objects.get_current().domain
        path = instance.interest.get_absolute_url()
        subject = "Your review and rating are now live"
        body = render_to_string(
            'approval-email.html',
            {
                'username': instance.user.username,
                'interest_url': 'https://' + domain + path,
                'email': settings.DEFAULT_FROM_EMAIL
            })
    else:
        subject = "Thank you for your rating and review"
        body = render_to_string(
            'submission-email.html',
            {
                'username': instance.user.username,
                'title': instance.title,
                'date_created': datetime.datetime.now(),
                'email': settings.DEFAULT_FROM_EMAIL
            })
    # Email sent to user
    send_mail(subject,
              body,
              '',
              [instance.user.email])


@receiver(post_save, sender=ReviewAndRating)
def from_user_rr(sender, instance, **kwargs):
    if instance.approved is False:
        # Email sent to admin
        send_mail("Review from User",
                  instance.interest.name + '\n\n' +
                  instance.title + '\n\n' +
                  instance.review,
                  '',
                  [config.DEFAULT_TO_EMAIL])


@receiver(post_save, sender=Comment)
def from_admin_comment(sender, instance, **kwargs):
    rr = instance.rr
    if instance.approved is True:
        domain = Site.objects.get_current().domain
        path = rr.interest.get_absolute_url()
        # Email sent to user
        send_mail("Your comment is now live",
                  'https://' + domain + path + '\n\n',
                   '',
                   [instance.user.email])
    else:
        # Email sent to user
        send_mail("Thank you for your comment",
                   instance.title,
                   '',
                   [instance.user.email])


@receiver(post_save, sender=Comment)
def from_user_comment(sender, instance, **kwargs):
    rr = instance.rr
    if instance.approved is False:
        # Email sent to admin
        send_mail("Comment from User",
                  rr.interest.name + '\n\n' +
                  instance.title + '\n\n' +
                  instance.body,
                  '',
                  [config.DEFAULT_TO_EMAIL])
