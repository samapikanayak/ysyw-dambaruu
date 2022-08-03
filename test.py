# def min_value(list):
#     lb = list[0]
#     for i in list:
#         if i < lb:
#             lb = i
#     return lb

# l = [11,3,29,10,100,4,54,-4,-9]
# lb = l[0]
# l1 = []

# for i in range(len(l)):
#     l1.append(min_value(l))
#     l.remove(min_value(l))

# print(l1)


# import boto3
# from botocore.exceptions import ClientError

# region = "ap-south-1"

# originationNumber = "8249118819"

# destinationNumber = "7205995905"

# message = ("This is a sample message sent from Amazon Pinpoint by using the "
#            "AWS SDK for Python (Boto 3).")

# applicationId = "491f67088075444a98e1693c503ef7dd"

# messageType = "TRANSACTIONAL"

# registeredKeyword = "myKeyword"

# senderId = "MySenderID"

# client = boto3.client('pinpoint',region_name=region)
# try:
#     response = client.send_messages(
#         ApplicationId=applicationId,
#         MessageRequest={
#             'Addresses': {
#                 destinationNumber: {
#                     'ChannelType': 'SMS'
#                 }
#             },
#             'MessageConfiguration': {
#                 'SMSMessage': {
#                     'Body': message,
#                     'Keyword': registeredKeyword,
#                     'MessageType': messageType,
#                     'OriginationNumber': originationNumber,
#                     'SenderId': senderId
#                 }
#             }
#         }
#     )

# except ClientError as e:
#     print(e.response['Error']['Message'])
# else:
#     print("Message sent! Message ID: "
#             + response['MessageResponse']['Result'][destinationNumber]['MessageId'])


import boto3

# # # Create an SNS client
# client = boto3.client(
#     "sns",
#     aws_access_key_id='AKIA3L45B6NMCQSQPFLL',
#     aws_secret_access_key='L9zNyeUFT66hg90fo1sLlOowP1f0XHB9diFvKvYi',
#     region_name='ap-south-1',
# )

# # Send your sms message.
# client.publish(
#     PhoneNumber="+918249118819",
#     Message="This is Amazon SNS service talking!"
# )

# def send_sms(*,PhoneNumber:str,Message:str) -> None:
#     client = boto3.client(
#         "sns",
#         aws_access_key_id='AKIA3L45B6NMCQSQPFLL',
#         aws_secret_access_key='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',
#         region_name='ap-south-1',
#         )

#     client.publish(
#         PhoneNumber=PhoneNumber,
#         Message=Message
#         )

# send_sms(PhoneNumber='+918249118819',Message='xxxx')




