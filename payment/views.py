from locale import currency
from urllib import response
from django.urls import reverse
from razorpay import Order
from YourSkoolYourWay.deps import razorpay_client
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import uuid

from courses.models import Standard
from . import serializers, models
from django.db import transaction
from django.conf import settings
from rest_framework.decorators import api_view

class CheckoutAPIView(GenericAPIView):
    serializer_class = serializers.OrderSerializer
    def post(self, request):
        currency = request.data["currency"]
        amount = request.data["amount"] * 100
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        user = request.user["id"]
        try:
            sum = 0
            for standard_id in request.data["standard_ids"]: 
                std = Standard.objects.get(id=standard_id)
                sum += std.price
            print(sum)
        except Standard.DoesNotExist:
                return Response({"status":"failed"})
        with transaction.atomic():
           
            order_obj = models.Order.objects.create(
                amount = amount,
                person_id = user
            )
            for standard_id in request.data["standard_ids"]: 
                try:
                    std = Standard.objects.get(id=standard_id)
                    order_obj.standard.add(Standard.objects.get(id=standard_id)) 
                except Standard.DoesNotExist:
                    return Response({"status":"failed"})
            
            razorpay_order = razorpay_client.order.create(
                {
                    'amount': amount, 
                    'currency': currency,
                    # 'reciept': order_obj.oid,  
                }
            )
            razorpay_order_id = razorpay_order['id']
            order_obj.razorpay_order_id = razorpay_order_id 
            order_obj.save()
            callback_url = ("https://" if request.is_secure() else "http://") + request.get_host() + reverse('payment-handler', args=[user]) 
            # callback_url = 'paymenthandler/'
            # we need to pass these details to frontend.
            response = {}
            response['razorpay_order_id'] = razorpay_order_id
            response['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            response['razorpay_amount'] = amount
            response['currency'] = currency
            response['username'] = order_obj.person.name
            #response['callback_url'] = callback_url
            order_obj.status = "incheckout"
            order_obj.save()
            return Response({"status": "success", "msg": "order created", "data": response})
        return Response({"status": "failed", "msg": "order failed", "data": ""}) 

# POST request will be made by Razorpay
# and it won't have the csrf token.
@api_view(["POST"])
def paymenthandler(request, user_id):
    # only accept POST request.
    try:
        # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        order = models.Order.objects.filter(
                razorpay_order_id=razorpay_order_id
            )

        # verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(
            params_dict)
        if result is None:
            data = {
                "status": "paid",
            }
            order.update(data)
            return Response({"msg": "payment success"},status=200)
        else:
            data = {
                "status": "failed",
            }
            order.update(data)
            return Response({"msg": "payment failed 2"},status=403)
    except Exception as e:
        print(e)
        data = {
                "status": "error",
            }
        # order.update(data)
        return Response({"msg": "payment failed 3"},status=402)
