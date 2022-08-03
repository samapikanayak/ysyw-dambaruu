from django.urls import path
from . import views

urlpatterns = [
    path("checkout/",views.CheckoutAPIView.as_view()),
    path("payment-handler/<user_id>/",views.paymenthandler, name='payment-handler')
]