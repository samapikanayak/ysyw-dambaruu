import razorpay
from django.conf import settings

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))