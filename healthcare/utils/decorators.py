from rest_framework.response import Response
import json
from django.utils import timezone
from healthcare.utils import error_messages,logging_utils
from django.conf import settings
from django.http.response import JsonResponse
from healthcare.models.master_model import OTPGenerator
from rest_framework import status


def otp_validation(func):
    def wrapper_otp_validation(*args, **kwargs):
        import pdb ;pdb.set_trace();
        try:
            verification_data = args[1].data
            otp_number = verification_data.get('otp_number')
            mobile_number = verification_data.get('mobile_number')
            email_id = verification_data.get('email_id')
            request = args[1]
            if not mobile_number and not email_id:
                return Response(
                    data = error_messages.MOBILE_NUMBER_OR_EMAIL_ID, status=status.HTTP_412_PRECONDITION_FAILED
                    )
            if not otp_number:
                return Response(
                    data = error_messages.DATA_NOT_PROVIDED, status=status.HTTP_412_PRECONDITION_FAILED
                )
            record = None
            if email_id:
                record = OTPGenerator.objects.filter(
                    otp_number=otp_number,
                    email_id=email_id
                )
            if not record:
                if mobile_number:
                    record = OTPGenerator.objects.filter(
                        otp_number=otp_number,
                        mobile_number=mobile_number
                    )
            if record: 
                if record.last().expired_at > timezone.now():  # if otp is not expired
                    # record = OTPGenerator.objects.filter(
                    #     otp_number=otp_number,
                    #     mobile_number=mobile_number
                    # )
                    request.otp_obj_list = record
                    return func(*args, **kwargs)
                else:
                    record.delete()
                    # OTPGenerator.objects.filter(
                    #     otp_number=otp_number,
                    #     mobile_number=mobile_number
                    # ).delete()
                    
                    return Response(
                        data=error_messages.OTP_EXPIRED,
                        status=status.HTTP_412_PRECONDITION_FAILED
                    )
            else:
                logging_utils.logger.info(f"decorator----------{otp_number}")
                return Response(
                    data=error_messages.OTP_VERIFICATION_FAILED,status=status.HTTP_412_PRECONDITION_FAILED
                    )
        except Exception as ex:
            return False

    return wrapper_otp_validation


