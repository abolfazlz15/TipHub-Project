from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from videos.models import Notification


@receiver(post_save, sender=Notification)
def sendEmail(sender, instance, created, **kwargs):
    if created and instance.send_email and instance.geter_user:
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('videos/send_email.html', {
            'user': instance.geter_user.email,
            'text': instance.text,
        })
        to_email = instance.geter_user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
