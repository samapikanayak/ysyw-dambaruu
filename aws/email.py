import threading,boto3
from django.conf import settings

ses = boto3.client('ses',region_name=settings.AWS_S3_REGION_NAME)


def send_email():
    ses.send_email(Source=settings.EMAIL_SOURCE,Destination={},Message={})
            #     Destination = {
            #         "ToAddresses":[
            #             # instance.email,
            #             # '3swayam@gmail.com',
            #             'samapikanayak03@gmail.com',
            #             # 'info@dambaruu.com'
                        
            #         ]
            #     },
            #     Message = {
            #         'Subject':{
            #             'Data':subject,
            #             'Charset':'UTF-8'
            #         },
            #         'Body':{
            #             'Text':{
            #                 'Data':body,
            #                 'Charset':'UTF-8'
            #             },
            #             'Html': {
            #         'Data': body_html,
            #         'Charset': 'UTF-8',
            #     },
            #         }
            #     }
            # )