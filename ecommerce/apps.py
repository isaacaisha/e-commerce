from django.apps import AppConfig


class PaypalIpnConfig(AppConfig):
    """django-paypal's ipn app doesn't declare an auto field, so the global
    DEFAULT_AUTO_FIELD (BigAutoField) makes Django want a migration inside
    site-packages. Pin it to AutoField to match the package's own migrations."""
    name = 'paypal.standard.ipn'
    label = 'ipn'
    default_auto_field = 'django.db.models.AutoField'
