from rest_framework.views import APIView
from rest_framework.parsers import JSONParser,MultiPartParser
from rest_framework import status
from healthcare.common import helper
from rest_framework.response import Response
from healthcare.common.serializers import MasterModelSerializers
from healthcare.utils.decorators import otp_validation
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import requests
from healthcare.utils import error_messages,shared,logging_utils
from reportlab.pdfgen import canvas
class SendOTP(APIView):
    parser_classes = (JSONParser,)

    def post(self,request):
        try:
            logging_utils.logger_info("send_otp-----------------")
            return helper.send_otp(self,request.data)
        except Exception as ex:
            logging_utils.main_exception(view="common view",exception=str(ex))
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
        
class UserRegistration(APIView):
    print("-----Regis---")
    #parser_classes = (JSONParser,)
    #@otp_validation
    def post(self,request):
        import pdb ;pdb.set_trace();
        try:
            request_data = request.data
            print("data", request_data)
            #request_data["otp_obj_list"] = request.otp_obj_list
            return helper.user_registration(self,request_data)
        except Exception as ex:
            return logging_utils.main_exception(view="send_otp_helper",exception=str(ex))


class GetAppointment(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.get_appointment(self,request_data)
        except Exception as ex:
            return logging_utils.main_exception(view="send_otp_helper",exception=str(ex))

        
class Logout(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            return helper.logout(self,request)
        except Exception as e:
            return logging_utils.main_exception(view="send_otp_helper",exception=str(e))

        

class GetFreeseachToken(APIView):
    parser_classes = (JSONParser,)

    def get(self, request):
        try:
            return helper.get_freesearch_token(self, request.data)
        except Exception as ex:
            return logging_utils.main_exception(view="send_otp_helper",exception=str(ex))

        
class LoginByOTP(APIView):
    parser_classes = (JSONParser,)

    @otp_validation
    def post(self, request):
        try:
            request_data = request.data
            request_data["otp_obj_list"] = request.otp_obj_list
            return helper.login_by_otp(self, request.data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class LoginByPassword(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        try:
            return helper.login_by_password(self, request.data)
        except Exception as ex:
            return logging_utils.main_exception(view="login_by_password",exception=str(ex))

class SetPassword(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            return helper.set_password(self, request)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
        
class ResetPassword(APIView):
    parser_classes = (JSONParser,)
    
    @otp_validation
    def post(self, request):
        try:
            request_data = request.data
            request_data["otp_obj_list"] = request.otp_obj_list
            return helper.reset_password(self, request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class ManageAppointment(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            request_data = shared.get_request_data(request)
            return helper.manage_appointment(self, request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class RefreshToken(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        try:
            return helper.refresh_token(self, request)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)


class UpdatePersonalDetails(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            request_data = shared.get_request_data(request)
            return helper.update_personelDetails(self, request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class GetPatientList(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            request_data = shared.get_request_data(request)
            return helper.get_patient_list(self, request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class GetDoctorList(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            request_data = shared.get_request_data(request)
            return helper.get_doctor_list(self, request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class ProceedPayment(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            request_data = shared.get_request_data(request)
            return helper.proceed_payment(self, request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class PaymentSuccess(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            request_data = shared.get_request_data(request)
            return helper.payment_success(self, request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
        
class GeneratePrescriptionPdf(APIView):
    # authentication_classes = (OAuth2Authentication,)
    # parser_classes = (MultiPartParser,)
    # permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            response = Response(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
            pdf_file_path = 'C://Users//OtherWork//Desktop//Helath_services//HealthcareProductModule//medical_services//healthcare//common//custormt.pdf'
            pdf_buffer = canvas.Canvas(pdf_file_path)
            # pdf_buffer = canvas.Canvas(response)
            pdf_buffer.drawString(100, 800, f"Customer Name: {request.data.get('customer_name')}")
            # Add other PDF content as needed
            pdf_buffer.save()

            return response
                # request_data = shared.get_request_data(request)
                # return helper.update_personelDetails(self, request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
        

class GetSymptoms(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            logging_utils.logger_info("GetSymptoms------------------------------------------")
            request_data = shared.get_request_data(request)
            return helper.get_symptoms(self,request_data)
        except Exception as ex:
            logging_utils.logger_info(f"View=admin_view, class=GetSymptoms, exception={ex}")
            return logging_utils.main_exception(self.get_view_name(), ex)
class AddTest(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.add_test(self,request_data)
        except Exception as ex:
            logging_utils.logger_info(f"View=admin_view, class=GetSymptoms, exception={ex}")
            return logging_utils.main_exception(self.get_view_name(), ex)
class GetTest(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.get_test_list(self,request_data)
        except Exception as ex:
            logging_utils.logger_info(f"View=admin_view, class=GetSymptoms, exception={ex}")
            return logging_utils.main_exception(self.get_view_name(), ex)
class GetPrescription(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.get_prescription_list(self,request_data)
        except Exception as ex:
            logging_utils.logger_info(f"View=common_view, class=GetPrescription, exception={ex}")
            return logging_utils.main_exception(self.get_view_name(), ex)