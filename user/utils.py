from twilio.rest import Client
import base64
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed,NotFound
from . import serializers

import smtplib, threading
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3



def threaded(func):
    def wrapper(*args,**kwargs):
        threading.Thread(target=func,args=args,kwargs=kwargs).start()
    
    return wrapper

def  get_object_or_404(Model,field_name=None,**fields):
    '''
    Parameters :- 
        a Model as parameter 
    Returns :- 
        object or 404 NotFound along with custom response
    '''
    try:
        return Model.objects.get(**fields)
    except Model.DoesNotExist:
        if field_name:
            raise NotFound({f"{field_name}":"Not found."})
        raise NotFound({f"{Model.__name__}":"Not found."})
    

def get_username_password(encoded_data):
    try:
        original_data = base64.b64decode(base64.b64decode(encoded_data)).decode()
        if original_data:
            username, password = original_data.split(":")
            return username, password
        else:
            raise AuthenticationFailed("authentication failed1")
    except base64.binascii.Error:
        raise AuthenticationFailed("authentication failed2")
    except UnicodeDecodeError:
        raise AuthenticationFailed("authentication failed3")
    except ValueError:
        raise AuthenticationFailed("authentication failed4")


def get_token(person):
    if person.status == "Approved" or person.status == "Pending":
        if person.role_id.role_id in [1,2,5,6]:
            serializer = serializers.AdminSerializer
        elif person.role_id.role_id in [4,8]:
            serializer = serializers.StudentSerializer
        else:
            serializer = serializers.TutorSerializer
        person_serialized_data = serializer(person).data
        return person_serialized_data
    else:
        raise AuthenticationFailed(
            "your account has been discarded. kindly contact admin to activate your account"
        )

BODY_TEXT = ("Amazon SES Test\r\n"
             "This email was sent through the Amazon SES SMTP "
             "Interface using the Python smtplib package."
            )


@threaded
def send_mail(*,subject: str, body_html: str, recipient: str) -> None:
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((settings.SENDERNAME, settings.SENDER))
    msg['To'] = recipient
    # Comment or delete the next line if you are not using a configuration set
    # msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(body_html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Try to send the message.
    try:  
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(settings.USERNAME_SMTP, settings.PASSWORD_SMTP)
        server.sendmail(settings.SENDER, recipient, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
    else:
        print ("Email sent!")
        
        
# @threaded
# def send_sms(*,PhoneNumber:str,Message:str) -> None:
#     client = boto3.client(
#     "sns",
#     aws_access_key_id='AKIA3L45B6NMCQSQPFLL',
#     aws_secret_access_key='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',
#     region_name='ap-south-1',
#     )

#     client.publish(
#         PhoneNumber=PhoneNumber,
#         Message=Message
#     )

@threaded
def send_sms(to,body):
    # Your Account SID from twilio.com/console
    account_sid = "ACdcadfb8b7890d3876218f91281f56217"
    # Your Auth Token from twilio.com/console
    auth_token  = "8258bd1e42bdcfd3b0a854bd6dcb9b8c"

    client = Client(account_sid, auth_token)

    client.messages.create(
        to=to, 
        from_="+14702601892",
        body=body)


