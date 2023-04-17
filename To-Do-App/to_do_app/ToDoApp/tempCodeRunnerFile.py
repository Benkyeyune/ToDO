from email1 import Create_Service
import base64
from  email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CLIENT_FILE = 'client.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCORES = ['https://mail.google.com/']

service = Create_Service(CLIENT_FILE,API_NAME,API_VERSION,SCORES)