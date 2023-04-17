from .email1 import Create_Service
import base64
from  email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CLIENT_FILE = '/home/calvin/to-do-app/to_do_app/ToDoApp/client.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCORES = ['https://mail.google.com/']

service = Create_Service(CLIENT_FILE,API_NAME,API_VERSION,SCORES)


def To_Do_email_notification(receivers_email,actual_email_message,email_subject):
    email_message = actual_email_message
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = receivers_email
    mimeMessage['subject'] = email_subject
    mimeMessage.attach(MIMEText(email_message,'html'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    message = service.users().messages().send(userId = 'me',body = {'raw':raw_string}).execute()
    return f'{actual_email_message} to {receivers_email} about {email_subject}'
    