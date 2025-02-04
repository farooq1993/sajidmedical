import requests
from rest_framework import status
from rest_framework.response import Response
from healthcare.utils import shared,error_messages,db_helper,constants,logging_utils
from healthcare.common.serializers import MasterModelSerializers,TransactionSerializer
from healthcare.patient.serializers import AppointmentMasterSerializer,PatientSerializer,AppointmentDetailsSerializer
from healthcare.doctor.serializers import DoctorSerializer
from django.contrib.auth.models import User
from django.conf import settings
import json
from healthcare.doctor.serializers import DoctorStaffManagementSerializer,TestMasterSerializer,PrescriptionSerializer
import razorpay
from healthcare.models.master_model import TransactionMaster
from healthcare.medical_admin.serializers import SymptomMasterSerializer,SymptomDetailSerializer


razorpay_client = razorpay.Client(
            auth=("rzp_test_0uGUp9kE1HEZiZ", "fBed4LmM6uUFjhqegVBgnwAN"))

def send_otp(self,request):
    try:
        logging_utils.logger_info("send_otp helper")
        mobile_number = request.get("mobile_number",None)
        email_id = request.get("email_id",None)
        action_type = request.get("action_type",None)

        if not action_type:
            return Response(data = error_messages.ACTION_TYPE_NOT_PROVIDED, status=status.HTTP_412_PRECONDITION_FAILED)
        if not mobile_number and not email_id:
           return Response(data = error_messages.MOBILE_NUMBER_OR_EMAIL_ID, status=status.HTTP_412_PRECONDITION_FAILED)

        if mobile_number:
            is_valid = shared.mobile_validator(mobile_number)
            if not is_valid:
              return Response(data=error_messages.INVALID_MOBILE_NUMBER, status=status.HTTP_412_PRECONDITION_FAILED)
            if action_type == constants.REGISTRATION:
                is_user,is_status = db_helper.get_user_master_data({
                    "mobile_number":mobile_number,
                    "data_type":constants.GET_FIRST_DATA
                    })
                if is_user:
                    return Response(data=error_messages.MOBILE_NO_EXISTS, status=status.HTTP_412_PRECONDITION_FAILED)
            otp = shared.generate_and_send_otp({"mobile_number":mobile_number})
            if not otp:
               return Response(data=error_messages.SEND_OTP_FAILURE, status=status.HTTP_412_PRECONDITION_FAILED) 
               
        elif email_id:
            is_valid = shared.email_id_regex(email_id)
            if not is_valid:
              return Response(data=error_messages.INVALID_EMAIL_ID, status=status.HTTP_412_PRECONDITION_FAILED)
            if action_type == constants.REGISTRATION:
                is_user,is_status = db_helper.get_user_master_data({
                    "email_id":email_id,
                    "data_type":constants.GET_FIRST_DATA
                    })
                if is_user:
                    return Response(data=error_messages.EMAIL_EXISTS, status=status.HTTP_412_PRECONDITION_FAILED)
            is_status = shared.generate_and_send_otp_on_email_id({"email_id":email_id})
            if not is_status:
               return Response(data=error_messages.SEND_OTP_FAILURE, status=status.HTTP_412_PRECONDITION_FAILED)    
        return Response(data=error_messages.OTP_SEND_SUCCESSFULLY,status=status.HTTP_200_OK)
    except Exception as ex:
        return logging_utils.main_exception(self.get_view_name(), ex)

    
def user_registration(self,request):
    import pdb ;pdb.set_trace();
    try:
        mobile_number = request.get("mobile_number",None)
        user_type = request.get("user_type",None)
    
        email_id = request.get("email_id",None)
        otp_obj_list = request.get("otp_obj_list",None)
        password = request.get("password",None)
        
        if not mobile_number and not email_id:
           return Response(data = error_messages.MOBILE_NUMBER_OR_EMAIL_ID, status=status.HTTP_200_OK)
        if not user_type:
           return Response(data = error_messages.USER_TYPE_NOT_PROVIDED, status=status.HTTP_200_OK)
        if mobile_number:
            is_valid = shared.mobile_validator(mobile_number)
            if not is_valid:
              return Response(data=error_messages.INVALID_MOBILE_NUMBER, status=status.HTTP_412_PRECONDITION_FAILED)
            user_obj,is_status = db_helper.get_user_master_data({
                "mobile_number":mobile_number,
                "data_type":constants.GET_FIRST_DATA
            })
            if user_obj:
                return Response(
                    data=error_messages.MOBILE_NO_EXISTS, status=status.HTTP_412_PRECONDITION_FAILED
                )
        if email_id:
            verified_email = shared.email_id_regex(email_id)
            if not verified_email:
               return Response(data=error_messages.INVALID_EMAIL_ID, status=status.HTTP_412_PRECONDITION_FAILED) 
            user_obj,is_status = db_helper.get_user_master_data({
            "email_id":email_id,
            "data_type":constants.GET_FIRST_DATA
            })
            if user_obj:
                return Response(
                    data=error_messages.EMAIL_EXISTS, status=status.HTTP_412_PRECONDITION_FAILED
                )
        user_type = db_helper.get_user_type({"user_type":user_type})
        if not user_type:
            return Response(
                data=error_messages.INVALID_USER_TYPE, status=status.HTTP_404_NOT_FOUND
            )
        request["user_type"] = user_type
        if email_id:
            if not shared.email_id_regex(email_id):
                return Response(
                data=error_messages.INVALID_EMAIL_ID, status=status.HTTP_412_PRECONDITION_FAILED
            )
        user_obj = MasterModelSerializers.insert(self,request)
        if user_obj:
            if password:
                password = shared.encrypt(password)
                passowrd_obj,created = db_helper.get_user_password({
                    "user_master":user_obj
                })
                passowrd_obj.password = password
                passowrd_obj.save()
            token = shared.get_auth_token(user_obj.user_name,settings.AUTH_TOKEN_PASSWORD)
            if token:
                registration_success = {
                    'success': True,
                    'data': {
                        'token': token,
                        'message': 'Registration Completed Successfully.',
                    }
                }
                otp_obj_list.delete()
                return Response(
                    data=registration_success, status=status.HTTP_200_OK
                )
            else:
               return Response(error_messages.AUTH_TOKEN_FAILURE, status.HTTP_412_PRECONDITION_FAILED)


    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

    
def get_appointment(self,request):
    try:
        user_obj = request.get("user_master_obj")
        action_type = request.get("action_type")
        if not action_type:
            return Response(data=error_messages.ACTION_TYPE_NOT_PROVIDED,status=status.HTTP_400_BAD_REQUEST)
        if user_obj.user_type.user_type_name.lower() == constants.PATIENT:
            request["patient_obj"] = user_obj
        elif user_obj.user_type.user_type_name.lower() == constants.DOCTOR:
            request["doctor_obj"] = user_obj
        else:
           return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        if action_type.lower() == constants.MASTER_DATA:
            request["data_type"] = constants.GET_LIST_WITH_COUNT
            appointment_obj,total_count = db_helper.get_appointment(request)
            if not total_count:
               return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            serialize_data = AppointmentMasterSerializer(appointment_obj,many=True).data
            translator_response = shared.basic_response_translator(
                is_success=True,
                total_result=total_count,
                data=serialize_data
            )
        elif action_type.lower() == constants.DETAIL_DATA:
            request["data_type"] = constants.GET_LIST_WITH_COUNT
            appointment_obj,total_count = db_helper.get_appointment_detail_data(request)
            if not total_count:
               return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            serialize_data = AppointmentDetailsSerializer(appointment_obj,many=True).data
            translator_response = shared.basic_response_translator(
                is_success=True,
                total_result=total_count,
                data=serialize_data
            )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def get_freesearch_token(self,request):
    try:
        guest_user = User.objects.get(username=settings.FREESEARCH_USERNAME)
        if not guest_user.check_password(settings.FREESEARCH_PASSWORD):
            guest_user.set_password(settings.FREESEARCH_PASSWORD)
            guest_user.save()
        token = shared.get_auth_token(settings.FREESEARCH_USERNAME, settings.FREESEARCH_PASSWORD)
        if token:
            data = {
                'success': True,
                'data': token
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=error_messages.AUTH_TOKEN_FAILURE, status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)


def login_by_otp(self,request):
    try:
        mobile_number = request.get('mobile_number')
        otp_obj_list = request.get("otp_obj_list",None)
        email_id = request.get('email_id')
        if not mobile_number and not email_id:
            return Response(data=error_messages.MOBILE_NUMBER_OR_EMAIL_ID, status=status.HTTP_412_PRECONDITION_FAILED)
        if mobile_number:
            is_valid = shared.mobile_validator(mobile_number)
            if not is_valid:
                return Response(data=error_messages.INVALID_MOBILE_NUMBER, status=status.HTTP_412_PRECONDITION_FAILED)
        is_user,is_status = db_helper.get_user_master_data({
            "mobile_number":mobile_number,
            "email_id":email_id,
            "data_type":constants.GET_FIRST_DATA

            })
        if not is_status:
            return Response(data=error_messages.USER_NOT_REGISTERED, status=status.HTTP_412_PRECONDITION_FAILED)
        if not is_user.is_active:
            return Response(data=error_messages.ACCOUNT_IS_DEACTIVATED, status=status.HTTP_412_PRECONDITION_FAILED)
        token = shared.get_auth_token(is_user.user_name, settings.AUTH_TOKEN_PASSWORD)
        if token:
            token['user_type'] = is_user.user_type.user_type_name
            data = {
                'success': True,
                'data': token
            }
            otp_obj_list.delete()
            return Response(data=data, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def login_by_password(self,request):
    try:
        mobile_number = request.get('mobile_number')
        email_id = request.get('email_id')
        password = request.get('password')
        if not mobile_number and not email_id:
            return Response(data=error_messages.MOBILE_NUMBER_OR_EMAIL_ID, status=status.HTTP_412_PRECONDITION_FAILED)
        if not password:
            return Response(data=error_messages.PASSWORD_NOT_PROVIDED, status=status.HTTP_412_PRECONDITION_FAILED)
        if mobile_number:
           is_valid = shared.mobile_validator(mobile_number)
           if not is_valid:
              return Response(data=error_messages.INVALID_MOBILE_NUMBER, status=status.HTTP_412_PRECONDITION_FAILED)
        if email_id:
            is_valid = shared.email_id_regex(email_id)
            if not is_valid:
                return Response(data=error_messages.INVALID_EMAIL_ID, status=status.HTTP_412_PRECONDITION_FAILED)
        is_user,is_status = db_helper.get_user_master_data({
            "mobile_number":mobile_number,
            "email_id":email_id,
            "data_type":constants.GET_FIRST_DATA
            })
        if not is_user:
            return Response(data=error_messages.UNREGISTERED_USER, status=status.HTTP_404_NOT_FOUND)
        get_password_obj = db_helper.get_user_password({"user_obj":is_user})
        if not get_password_obj:
            return Response(data=error_messages.PASSWORD_NOT_SET, status=status.HTTP_404_NOT_FOUND)
        decrypt_password = shared.decrypt(get_password_obj.password)
        if password !=decrypt_password:
            return Response(data=error_messages.INVALID_CREDENTIALS, status=status.HTTP_412_PRECONDITION_FAILED)
        token = shared.get_auth_token(is_user.user_name, settings.AUTH_TOKEN_PASSWORD)
        if token:
            data = {
                'success': True,
                'data': token
            }
            return Response(data=data, status=status.HTTP_200_OK)
    except Exception as ex:
        logging_utils.logger_info(str(ex))
        return logging_utils.main_exception(view="login_by_password",exception=str(ex))

       
def logout(self,request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split()[-1]
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            'client_id': settings.AUTH_CLIENT_ID,
            'client_secret': settings.AUTH_SECRET_ID,
            'token': token
        }
        requests.post(
            url=settings.REVOKE_TOKEN,
            data=payload,
            headers=headers
        )
        return Response(error_messages.LOGOUT_MESSAGE, status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)


def set_password(self,request):
    try:
        request_data = request.data
        new_password = request_data.get("password",None)
        confirm_password = request_data.get("confirm_password",None)

        user_obj,is_status = db_helper.get_user_master_data({
            "user":request.user,
            "data_type":constants.GET_FIRST_DATA
            })
        if not user_obj:
            return Response(data=error_messages.INVALID_REQUEST, status=status.HTTP_412_PRECONDITION_FAILED)
        if not new_password:
            return Response(data=error_messages.PASSWORD_NOT_PROVIDED, status=status.HTTP_412_PRECONDITION_FAILED)
        if not new_password:
            return Response(data=error_messages.CONFIRM_PASSWORD_NOT_PROVIDED, status=status.HTTP_412_PRECONDITION_FAILED)
        if new_password !=confirm_password:
            return Response(data=error_messages.BOTH_PASSWORD_NOT_MATCHED, status=status.HTTP_412_PRECONDITION_FAILED)
        validate_password = shared.password_regex(new_password)
        if not validate_password:
            return Response(data=error_messages.INVALID_PASSWORD, status=status.HTTP_412_PRECONDITION_FAILED)
        password = shared.encrypt(new_password)
        
        passowrd_obj,created = db_helper.get_user_password({
            "user_master":user_obj
        })
        passowrd_obj.password = password
        passowrd_obj.save()

        return Response(data=error_messages.DATA_INSERTED, status=status.HTTP_200_OK)

    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

def reset_password(self,request):
    try:
        mobile_number = request.get("mobile_number",None)
        email_id = request.get("email_id",None)
        new_password = request.get("new_password",None)
        otp_obj_list = request.get("otp_obj_list",None)
        
        user_obj,is_status = db_helper.get_user_master_data({
            "email_id":email_id,
            "mobile_number":mobile_number,
            "data_type":constants.GET_FIRST_DATA
            })
        if not new_password:
            return Response(data=error_messages.PASSWORD_NOT_PROVIDED, status=status.HTTP_412_PRECONDITION_FAILED)
        validate_password = shared.password_regex(new_password)
        if not validate_password:
            return Response(data=error_messages.INVALID_PASSWORD, status=status.HTTP_412_PRECONDITION_FAILED)
        password = shared.encrypt(new_password)
        
        passowrd_obj,is_created = db_helper.get_user_password({
            "user_master":user_obj
        })
        passowrd_obj.password = password
        passowrd_obj.save()
        otp_obj_list.delete()
        return Response(data=error_messages.DATA_INSERTED, status=status.HTTP_200_OK)
        
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def manage_appointment(self,request):
    try:
        user_master_obj = request.get("user_master_obj",None)
        if not user_master_obj:
           return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        appointment_id = request.get("appointment_id",None)
        action_type = request.get("action_type",None)
        if not action_type:
           return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        if action_type == constants.DELETE:
            appointment_lst = db_helper.get_appointment(request)
            if not appointment_lst:
               return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            appointment_lst.delete()
            return Response(data=error_messages.APPOINTMENT_DELETE,status=status.HTTP_404_NOT_FOUND)
        elif action_type == constants.UPDATE:
            if not appointment_id:
                return Response(data=error_messages.DATA_NOT_PROVIDED, status=status.HTTP_412_PRECONDITION_FAILED)
            appointment_obj,is_status = db_helper.get_appointment({"appointment_id":appointment_id,"data_type":constants.GET_FIRST_DATA})
            is_status= AppointmentMasterSerializer.update_data(self,request,appointment_obj)
            if is_status:
               return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

def refresh_token(self,request):
    try:
        refresh_token = request.data.get('refresh_token', None)
        if not refresh_token:
            return Response(
                data=error_messages.INVALID_REQUEST,
                status=status.HTTP_412_PRECONDITION_FAILED
            )
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {
            'grant_type': 'refresh_token',
            'client_id': settings.AUTH_CLIENT_ID,
            'client_secret': settings.AUTH_SECRET_ID,
            'token type': 'Bearer',
            'refresh_token': refresh_token
        }
        URL = settings.SERVER_PROTOCOLS + settings.AUTH_TOKEN_URL
        response = requests.post(url=URL, data=payload, headers=headers)
        if response.ok:
            loaded_json = json.loads(response.text)
            response = {
                'success': True,
                'data': loaded_json
            }
            return Response(data=response, status=status.HTTP_200_OK)
        loaded_json = json.loads(response.text)
        response = {
            'success': False,
            'data': {
                'message': 'Something wwnt wrong.',
                'error': loaded_json
            }
        }
        return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

def update_personelDetails(self,request):
    try:
        user_obj = db_helper.get_user_master_data({
            "user":request.get("user"),
            "data_type":constants.GET_FIRST_DATA
            })
        if user_obj.user_type.user_type_name.lower() in (constants.DOCTOR,constants.PATIENT):
            user_obj = MasterModelSerializers.insert(self,request,user_obj)
        elif user_obj.user_type.user_type_name.lower() == constants.DOCTOR_STAFF:
            user_obj = DoctorStaffManagementSerializer.update_staff_record(self,request,user_obj)
        return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def get_patient_list(self,request):
    try:
        request["user_type_id"] = 3
        request["data_type"] = constants.GET_LIST_WITH_COUNT
        patient_list,total_count = db_helper.get_user_master_data(request)
        if not total_count:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        serialize_data = PatientSerializer(patient_list,many=True).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result=total_count,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def get_doctor_list(self,request):
    try:
        request["user_type_id"] = 2
        request["data_type"] = constants.GET_LIST_WITH_COUNT
        patient_list,total_count = db_helper.get_user_master_data(request)
        if not total_count:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        serialize_data = DoctorSerializer(patient_list,many=True).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result=total_count,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def proceed_payment(self,request):
    try:
        appointment_code = request.get("appointment_code")
        amount = request.get("amount")
        
        if not appointment_code or not amount:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        appointment_obj,is_status = db_helper.get_appointment({
            "appointment_code":appointment_code,"data_type":constants.GET_FIRST_DATA
            })
        if not appointment_obj:
            return Response(data=error_messages.APPOINTMENT_RECORD_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        # transaction_obj,is_status = db_helper.get_transaction_data({
        #     "appointment_obj":appointment_obj,
        #     "is_paid":constants.IN_ACTIVE,
        #     "data_type":constants.GET_FIRST_DATA
        #     })
        # if not transaction_obj:
        data = razorpay_client.order.create({
            "amount": int(amount) * 100,
            "currency": "INR",
            "receipt": appointment_code, 
            "payment_capture": "1"
            })
        resp_data = razorpay_client.order.create(data=data)
        transaction_obj = TransactionMaster.objects.create(
            appointment = appointment_obj,amount=amount, razorpay_order_id=resp_data.get('id')
        )
        serializer_data = TransactionSerializer(transaction_obj).data
        # translator_response = shared.basic_response_translator(
        #     is_success=True,
        #     total_result=None,
        #     data=serializer_data
        # )
        data = {
            "payment": resp_data,
            "order": serializer_data
            }
        return Response(data=data,status=status.HTTP_200_OK)
    except Exception as ex:
        logging_utils.logger_info(f"helper=common_helper, helper=proceed_payment, exception={ex}")
        return logging_utils.main_exception(self.get_view_name(), ex)

def payment_success(self,request):
    try:
        logging_utils.logger_info("payment_success-----------------------------helper1-------------")
        razorpay_payment_id = request.get('razorpay_payment_id')
        razorpay_order_id = request.get('razorpay_order_id')
        razorpay_signature = request.get('razorpay_signature')
        
        transaction_obj,is_status = db_helper.get_transaction_data({
            "razorpay_order_id":razorpay_order_id,
            "data_type":constants.GET_FIRST_DATA
            })
        if not transaction_obj:
            return Response(data=error_messages.APPOINTMENT_RECORD_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        data = {
        'razorpay_order_id': razorpay_order_id, 
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
        }
        logging_utils.logger_info(f"payment_success-----------------------------helper23-------------{data}")
        logging_utils.logger_info("payment_success-----------------------------helper2-------------")
        check = razorpay_client.utility.verify_payment_signature(data)
        logging_utils.logger_info(f"payment_success-----------------------------helper7-------------,{check}")
        if not check:
            logging_utils.logger_info(f"check---{check}")
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
        appointment_obj,is_status = db_helper.get_appointment({
            "appointment_id":transaction_obj.appointment_id,"data_type":constants.GET_FIRST_DATA
            })
        logging_utils.logger_info("payment_success-----------------------------helper3-------------")
        if appointment_obj:
            appointment_obj.is_paid = True
            appointment_obj.save()
        transaction_obj.razorpay_payment_id = razorpay_payment_id
        transaction_obj.razorpay_signature = razorpay_signature
        transaction_obj.is_paid = True
        transaction_obj.save()
        logging_utils.logger_info("payment_success-----------------------------helper4-------------")
        return Response(data=error_messages.PAYMENT_SUCCESS,status=status.HTTP_200_OK)
    except Exception as ex:
        logging_utils.logger_info(str(ex))
        logging_utils.helper_error(view="common_helper", function_name="payment_success", exception=str(ex))
        logging_utils.logger_info(f"helper=common_helper, helper=proceed_success, exception={ex}")
        return logging_utils.main_exception(self.get_view_name(), ex)
    
def get_symptoms(self,request):
    try:
        logging_utils.logger_info("GetSymptoms-----------------------------helper2-------------")
        user_obj = request.get("user_master_obj",None)
        action_type = request.get("action_type",None)
        symptom_id = request.get("symptom_id",None)
        # if user_obj.user_type.user_type_name.lower() !=constants.ADMIN:
        #     return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        if not action_type:
               return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        if action_type == constants.MASTER_DATA:
            request["data_type"] = constants.GET_LIST_WITH_COUNT
            records,total_count = db_helper.get_symptom_master_data(request)
            if total_count:
                serialize_data = SymptomMasterSerializer(records,many=True).data
                if serialize_data:
                    translator_response = shared.basic_response_translator(
                        is_success=True,
                        total_result=total_count,
                        data=serialize_data
                    )
                    return Response(data=translator_response,status=status.HTTP_200_OK)
            else:
               return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        elif action_type == constants.DETAIL_DATA:
            # if not symptom_id:
            #    return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
            request["data_type"] = constants.GET_LIST_WITH_COUNT
            records,total_count = db_helper.get_symptom_detail_data(request)
            if total_count:
                serialize_data = SymptomDetailSerializer(records,many=True).data
                if serialize_data:
                    translator_response = shared.basic_response_translator(
                        is_success=True,
                        total_result=total_count,
                        data=serialize_data
                    )
                    return Response(data=translator_response,status=status.HTTP_200_OK)
            else:
                return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        logging_utils.logger_info(f"helper=common_helper, func=get_symptoms, exception={ex}")
        return logging_utils.main_exception(self.get_view_name(), ex)
    
def add_test(self, request):
    try:
        user_obj = request.get("user_master_obj")
        if user_obj.user_type.user_type_name.lower() not in (constants.DOCTOR,constants.DOCTOR_STAFF,constants.ADMIN):
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        
        if not request.get("name"):
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        get_test_obj = db_helper.get_test_master_data(request)
        if get_test_obj:
            return Response(data=error_messages.DATA_ALREADY_EXISTS,status=status.HTTP_400_BAD_REQUEST)
        serializer_data = TestMasterSerializer.insert(self, request)
        if serializer_data:
            return Response(data=error_messages.DATA_INSERTED,status=status.HTTP_200_OK)
    except Exception as ex:
        logging_utils.logger_info(f"helper=common_helper, func=add_test, exception={ex}")
        return logging_utils.main_exception(self.get_view_name(), ex)
    
def get_test_list(self,request):
    try:
        user_obj = request.get("user_master_obj")
        if user_obj.user_type.user_type_name.lower() not in (constants.DOCTOR,constants.DOCTOR_STAFF,constants.ADMIN):
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        request["data_type"] = constants.GET_LIST_WITH_COUNT
        records,total_count = db_helper.get_test_master_data(request)
        if not total_count:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        serializer_data = TestMasterSerializer(records,many=True).data
        if serializer_data:
            translator_response = shared.basic_response_translator(
                is_success=True,
                total_result=total_count,
                data=serializer_data
            )
            return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        logging_utils.logger_info(f"helper=common_helper, func=get_test_list, exception={ex}")
        return logging_utils.main_exception(self.get_view_name(), ex)
    
def get_prescription_list(self,request):
    try:
        user_obj = request.get("user_master_obj", None)
        if user_obj.user_type.user_type_name.lower() == constants.DOCTOR:
            request["doctor_obj"] = user_obj
        elif user_obj.user_type.user_type_name.lower() == constants.DOCTOR_STAFF:
            request["doctor_id"] = user_obj.doctor_id
        elif user_obj.user_type.user_type_name.lower() == constants.PATIENT:
            request["patient_obj"] = user_obj
        request["data_type"] = constants.GET_LIST_WITH_COUNT
        records,total_count = db_helper.get_prescription_data(request)
        if not total_count:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        serializer_data = PrescriptionSerializer(records,many=True).data
        if serializer_data:
            translator_response = shared.basic_response_translator(
                is_success=True,
                total_result=total_count,
                data=serializer_data
            )
            return Response(data=translator_response,status=status.HTTP_200_OK)

    except Exception as ex:
        logging_utils.logger_info(f"helper=common_helper, func=get_prescription_list, exception={ex}")
        return logging_utils.main_exception(self.get_view_name(), ex)
    
from django.contrib.auth.backends import ModelBackend
from healthcare.models.master_model import User

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)  # Use correct field
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None