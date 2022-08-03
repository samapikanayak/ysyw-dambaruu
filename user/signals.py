from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Person
from .tasks import send_html_mail

import threading

from django.conf import settings
# from ..aws.email import send_email

from .utils import send_mail



@receiver(post_save, sender=Person)
def person_post_save(sender, instance, created, **kwargs):
    if created:
        if not instance.is_active and instance.status=="Pending":
            link = settings.REACT_FRONTEND_PASSWORD_SET_URL + str(instance.id) + "/" +instance.password_creation_token
            context = {"link":link,"fullname":instance.name}
            # threading.Thread(target=send_html_mail,args=('subject' ,instance.email,'mail/activation_mail.html',context)).start()
            subject = 'Account activation'
            body_html = f'''<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Activation</title>
                </head>
                <body>
                    <h1>Activation mail</h1>
                    <h2>Hello, {instance.name}</h2>
                    <a href="{link}">Activate Account</a>
                </body>
                </html>'''
            send_mail(subject=subject,body_html=body_html,recipient=instance.email)