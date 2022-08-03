from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_html_mail(subject, to, template, context, from_email="From <yourskoolyourway@gmail.com>"):
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
