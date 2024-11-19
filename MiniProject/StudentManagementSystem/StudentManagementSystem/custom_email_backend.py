# custom_email_backend.py
import ssl
from django.core.mail.backends.smtp import EmailBackend


class CustomEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        kwargs['ssl_context'] = ssl._create_unverified_context()
        super().__init__(*args, **kwargs)
