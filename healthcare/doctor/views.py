from rest_framework.views import APIView
from rest_framework.parsers import JSONParser,MultiPartParser
from rest_framework import status
from healthcare.doctor import helper
from rest_framework.response import Response
from healthcare.utils.decorators import otp_validation
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from healthcare.utils import error_messages,shared
class GetProfile(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.get_profile(self,request_data)
        except Exception as ex:
            return False
class CreateAppointment(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.create_appointment(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class AddStaff(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.add_staff(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
        
class GetStaff(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.get_staff(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class ManageStaff(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.manage_staff(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class AddMedicine(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.add_medicine(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
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
class CreatePrescription(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            file = request.FILES.get('file')
            request_data["file"] = file
            return helper.create_prescription(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class GetPrescription(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,MultiPartParser)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            user = request.user
            request_data = request.data
            request_data["user"] = user
            return helper.get_prescription(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class ManagePrescription(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            user = request.user
            request_data = request.data
            request_data["user"] = user
            return helper.manage_prescripton(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class ManageAccount(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.manage_account(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class GetStaffProfile(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.get_staff_profile(self,request_data)
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

