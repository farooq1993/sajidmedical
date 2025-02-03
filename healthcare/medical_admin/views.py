from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from healthcare.medical_admin import helper
from rest_framework.response import Response
from healthcare.utils.decorators import otp_validation
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from healthcare.utils import error_messages,shared,logging_utils

class AppointmentHistory(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.appointment_history(self,request_data)
        except Exception as ex:
            return False
class GetMedicine(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.get_medicine(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class ManageMedicine(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.manage_medicine(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
        
class GetDoctor(APIView):
    authentication_classes = (OAuth2Authentication)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            return helper.get_doctor(self,request.data)
        except Exception as ex:
            return False

class ManageDoctor(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.manage_doctor(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
        
class GetPatient(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated)

    def post(self,request):
        try:
            return helper.get_patient(self,request.data)
        except Exception as ex:
            return False
        
class ManagePatient(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.manage_patient(self,request_data)
        except Exception as ex:
            logging_utils.logger_info(f"View=admin_view, class=manage_patient, exception={ex}")
            return logging_utils.main_exception(self.get_view_name(), ex)
        
        
class AddSymptoms(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.add_symptoms(self,request_data)
        except Exception as ex:
            logging_utils.logger_info(f"View=admin_view, class=Add_symptoms, exception={ex}")
            return logging_utils.main_exception(self.get_view_name(), ex)
class GetSymptoms(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.get_symptoms(self,request_data)
        except Exception as ex:
            logging_utils.logger_info(f"View=admin_view, class=GetSymptoms, exception={ex}")
            return logging_utils.main_exception(self.get_view_name(), ex)
class ManageSymptoms(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.manage_symptoms(self,request_data)
        except Exception as ex:
            logging_utils.logger_info(f"View=admin_view, class=ManageSymptoms, exception={ex}")
            return logging_utils.main_exception(self.get_view_name(), ex)
            