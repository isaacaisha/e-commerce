from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'

    # Set up Paypal IPN Signal
    def ready(self):
        import payment.hooks
