from django.test import TestCase
from .sendemail import To_Do_email_notification


# Create your tests here.

def test_email():
    assert To_Do_email_notification('example@gmail.com','hey its me','test') == 'hey its me to example@gmail.com about test'
