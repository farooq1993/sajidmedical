from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from healthcare.patient import helper
from rest_framework.response import Response
from healthcare.utils.decorators import otp_validation
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from healthcare.utils import shared

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
    
    def post(self, request):
        try:
            request_data = shared.get_request_data(request)
            print("Request Data:", request_data)  # Log the incoming request data
            return helper.create_appointment(self, request_data)
        except Exception as ex:
            print("Error in creating appointment:", ex)
            return Response({"error": "Internal Server Error"}, status=500)

class AddFamilyMember(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    
    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.add_family_member(self,request_data)
        except Exception as ex:
            return False
class GetFamilyDetails(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    
    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.get_family_member(self,request_data)
        except Exception as ex:
            return False
class ManageFamilyMember(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    
    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.update_family_detail(self,request_data)
        except Exception as ex:
            return False
class ManageAccount(APIView):
    authentication_classes = (OAuth2Authentication,)
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    
    def post(self,request):
        try:
            request_data = shared.get_request_data(request)
            return helper.manage_account(self,request_data)
        except Exception as ex:
            return False
