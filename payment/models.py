from re import I
from statistics import mode
from django.db import models
from user.models import CommonFields
from courses.models import Standard 
from user.models import Person
from uuid import uuid4

class Order(CommonFields):
    status_choice = (
        ('paid','paid'), # order paid and property Booked
        ('failed','failed'), # order failed due to user inactivity    
        ('incheckout','incheckout'), # order in checkout
        ('refunded','refunded'), # user cancel
        ('canclled','canclled'), # after user cancel some of times a refund will initiate after 24 hour and save to db and save to cancel table
        ('error','error'), # some error may occur from razorpay
    )
   
    oid = models.CharField(max_length=40) 
    standard = models.ManyToManyField(Standard)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20,choices=status_choice)
    amount = models.IntegerField()
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.oid:
            self.oid = f"YSYWOID{uuid4().hex}" 
        super(Order, self).save(*args, **kwargs)

        

class Subscrtion(CommonFields):
    ...
    




class CancelOrder(models.Model):
    # user
    # booking_order_id
    # msg_body if any then initiate 
    ...


class Refund(models.Model):
    ...
    # razorpay_id
    # user id
    # order id
    # status (success, in_processed)

   
class Invoice(models.Model):
    ...
    # razorpay_id
    # user id
    # order id
   

class Payout(models.Model):
    ...
    # razorpay_id
    # user id
    # order id
    # status (success, in_processed)
