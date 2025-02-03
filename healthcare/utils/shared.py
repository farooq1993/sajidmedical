import random
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime, timedelta
from healthcare.models.master_model import OTPGenerator,User, User
from twilio.rest import Client
from healthcare.utils import constants,error_messages,logging_utils
from django.conf import settings
import requests
import json
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from django.core.mail import EmailMessage
from rest_framework.response import Response
from rest_framework import status
# from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


def get_otp():
    return str(random.randint(1000, 9999))

def mobile_validator(mobile_no):
    validator = RegexValidator(
        regex=r'^\d{9,15}$',
        message="Invalid mobile number"
    )
    try:
        validator(mobile_no)
        return True
    except Exception:
        return False
    
def email_id_regex(email_id):
    validator = RegexValidator(
        regex=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}',
        message="Invalid email id"
    )
    try:
        validator(email_id)
        return True
    except Exception as ex:
        return False

def generate_and_send_otp(request):
    try:
        logging_utils.logger_info("generate_and_send_otp")
        mobile_number = request.get("mobile_number")
        expired_at = timezone.now() + timedelta(minutes=15)
        obj_deleted = OTPGenerator.objects.filter(mobile_number=mobile_number).delete()
        logging_utils.logger_info(f"record deleted----{obj_deleted}")
        otp_number = get_otp()
        obj=OTPGenerator.objects.create(
            otp_number=otp_number, mobile_number=mobile_number, expired_at=expired_at)
        logging_utils.logger_info(f"record save----{obj}")
        message = constants.OTP_FOR_LOGIN.format(otp_number)
        account_sid = 'AC79b1e763bc7d3a540f7520fbe78bbf6b'
        auth_token = 'e3a19e7e542929dd76b9d00980e1d03b'
        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            from_='+14128475074',
            body=message,
            # to='+91' + mobile_number
            to='+919971141950'
            )
        return msg
    except Exception as ex:
        logging_utils.main_exception(view="generate_and_send_otp",exception=str(ex))
        return False
    
def basic_response_translator(is_success, data, total_result=None, start=None, end=None, total_count=None):
    response_translator = {}
    response_translator["success"] = is_success
    if total_result:
        response_translator["total_result"] = total_result
    elif total_result == 0:
        response_translator["total_result"] = total_result
    if start:
        response_translator["start"] = start
    elif start == 0:
        response_translator["start"] = start
    if total_count:
        response_translator["total_count"] = total_count
    elif total_count == 0:
        response_translator["total_count"] = 0
    if end:
        response_translator["end"] = end
    elif end == 0:
        response_translator["end"] = end
    response_translator["data"] = data
    return response_translator


def get_auth_token(username, password):
    try:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': settings.AUTH_CLIENT_ID,
            'client_secret': settings.AUTH_SECRET_ID
        }
        URL = settings.SERVER_PROTOCOLS + settings.AUTH_TOKEN_URL
        api_response = requests.post(
            url=URL,
            data=payload,
            headers=headers
        )
        if api_response.ok:
            return json.loads(api_response.text)
        return False
    except Exception as ex:
        return False
    
def generate_random_number(length):
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return random.randint(range_start, range_end)

def user_code(user_type):
    return user_type.upper() + str(generate_random_number(8))

def decrypt(password):
    try:
        data = b64decode(password)
        bytes = PBKDF2("edp@$3#drishti".encode("utf-8"),
                       "dRishtI".encode("utf-8"), 48, 128)
        iv = bytes[0:16]
        key = bytes[16:48]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        text = cipher.decrypt(data)
        password = text[:-text[-1]].decode("utf-8")
        return password
    except Exception as ex:
        return False
    
def r_pad(payload, block_size=16):
    length = block_size - (len(payload) % block_size)
    return payload + chr(length) * length

def encrypt(password):
    try:
        bytes = PBKDF2("edp@$3#drishti".encode("utf-8"),
                    "dRishtI".encode("utf-8"), 48, 128)
        iv = bytes[0:16]
        key = bytes[16:48]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        text = cipher.encrypt(r_pad(password).encode("utf-8"))
        text = b64encode(text)
        text = text.decode("utf-8")
        return text
    except Exception as ex:
        return False
    
def password_regex(password):
    validator = RegexValidator(
        regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#()+,-./:;<=>[\]^_`{|}~\'\\\"])[A-Za-z\d@$!%*?&#()+,-./:;<=>[\]^_`{|}~\'\\\"]{7,}$',
        message="Password should be Min. 7 Characters, Should contain one number, one uppercase character, one lowercase character, one special character."
    )
    try:
        validator(password)
        return True
    except Exception as ex:
        return False
    
def send_otp_email_body(otp):
    body = '''\
                <html>
                <head></head>
                <body>
                    <p>
                        Dear Sir,<br><br><br>
                        <b>'''+f'This is your OTP {otp} for login Medical Services App'+'''</b><br><br>
                        Medical Services.
                    </p>
                </body>
                </html>
            '''
    return body
    

def send_email(sub, body,email_id,file=None):
    try:
        email = EmailMultiAlternatives(sub, to=[email_id])
        if file:
           email.attach('precription.pdf', file)
        email.attach_alternative(body, "text/html")
        is_sent = email.send()
        if is_sent:
            return True
        return Response(data=error_messages.SEND_EMAIL_FAILURE, status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG, status=status.HTTP_412_PRECONDITION_FAILED)
    
def get_request_data(request):
    user = request.user
    request_data = request.data
    # request_data["user"] = user
    request_data["user_master_obj"] = User.objects.filter(user=user).first()
    return request_data

def generate_and_send_otp_on_email_id(request):
    try:
        email_id = request.get("email_id",None)
        expired_at = timezone.now() + timedelta(minutes=15)
        OTPGenerator.objects.filter(email_id=email_id).delete()
        otp_number = get_otp()
        OTPGenerator.objects.create(
            otp_number=otp_number, email_id=email_id, expired_at=expired_at
        )
        mail_body = send_otp_email_body(otp_number)
        is_status = send_email("Medical Service Otp verification",mail_body,email_id)
        if is_status:
            return True
        else:
            return False
    except Exception as ex:
        return False
    
def time_converter(time_to_convert):

        time_slot_to_12_hr = datetime.strptime(time_to_convert, "%I:%M %p")
        time_slot_to_24_hr = time_slot_to_12_hr.strftime("%H:%M")
        return time_slot_to_24_hr