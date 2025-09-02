# /home/siisi/e-commerce/payment/hooks.py

import time

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings

from .models import Order


@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    # Wait 9 seconde for Paypal to send IPN data
    time.sleep(9)

    # Grab the Paypal sends
    paypal_obj = sender
    # Grab the Invoice
    my_invoice = str(paypal_obj.invoice)
    #print(f'paypal_obj:\n{paypal_obj}\n\npaypal_obj.mc_gross:\n{paypal_obj.mc_gross}')

    # Match the Paypal invoice to the Order invoice
    # Look up the Order
    my_Order = Order.objects.get(invoice=my_invoice)

    # Record the Order was Paid
    my_Order.paid = True
    # Save the Order
    my_Order.save()
