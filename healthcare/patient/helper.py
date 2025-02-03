import requests
from rest_framework import status
from rest_framework.response import Response
from healthcare.utils import shared,error_messages,db_helper,constants,logging_utils
from healthcare.patient.serializers import PatientSerializer,AppointmentMasterSerializer,AddFamilyMemberSerializer,AppointmentDetailsSerializer

def get_profile(self,request):
    try:
        user_obj = request.get("user_master_obj")
        if user_obj.user_type.user_type_name.lower() !=constants.PATIENT:
            return Response(data=error_messages.INVALID_REQUEST,status=status.HTTP_412_PRECONDITION_FAILED)
        serialize_data = PatientSerializer(user_obj,many=False).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result = None,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return False
    
def create_appointment(self,request):
    try:
        user_obj = request.get("user_master_obj",None)
        if user_obj.user_type.user_type_name.lower()!=constants.PATIENT:
            return Response(
                data=error_messages.INVALID_REQUEST, status=status.HTTP_412_PRECONDITION_FAILED
            )
        doctor_id = request.get("doctor_id",None)
        if not doctor_id:
            return Response(
                data=error_messages.DOCTOR_DETAIL_NOT_PROVIDED, status=status.HTTP_412_PRECONDITION_FAILED
            )
        request['user_master_id'] = doctor_id
        request['data_type'] = constants.GET_FIRST_DATA
        request['user_type_id'] = 2
        doctor_obj,is_status = db_helper.get_user_master_data({
                "user_type_id":2,
                "user_master_id":doctor_id,
                "data_type":constants.GET_FIRST_DATA        
        })
        if not doctor_obj:
            return Response(
                data=error_messages.DOCTOR_NOT_FOUND, status=status.HTTP_404_NOT_FOUND
            )
        request["patient_obj"] = user_obj
        request["doctor_obj"] = doctor_obj
        is_appointment = AppointmentMasterSerializer.insert(self,request)
        if is_appointment:
            appointment_obj,is_status = db_helper.get_appointment({
                "appoitnemnt_id":is_appointment.id,"data_type":constants.GET_FIRST_DATA
                })
            serialized_data = AppointmentMasterSerializer(appointment_obj,many=False).data
            is_appointment_detail_created = AppointmentDetailsSerializer.insert(self,request,is_appointment)
            if is_appointment_detail_created:
                translator_response = shared.basic_response_translator(
                is_success=True,
                total_result=None,
                data=serialized_data
                )
                return Response(data=translator_response,status=status.HTTP_200_OK)
            
    except Exception as ex:
        logging_utils.logger_info("patient_helper","create_appointment",ex)
        return logging_utils.main_exception(self.get_view_name(), ex)
    
def add_family_member(self,request):
    try:
        user_obj = request.get("user_master_obj",None)
        if user_obj.user_type.user_type_name.lower()!=constants.PATIENT:
            return Response(
                data=error_messages.INVALID_REQUEST, status=status.HTTP_412_PRECONDITION_FAILED
            )
        request["patient_obj"] = user_obj
        is_family_added = AddFamilyMemberSerializer.insert(self,request)
        if is_family_added:
            return Response(
                    data=error_messages.DATA_INSERTED, status=status.HTTP_200_OK
                )
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def get_family_member(self,request):
    try:
        user_obj = request.get("user_master_obj")
        if user_obj.user_type.user_type_name.lower()!=constants.PATIENT:
            return Response(
                data=error_messages.INVALID_REQUEST, status=status.HTTP_412_PRECONDITION_FAILED
            )
        request["patient_obj"] = user_obj
        request["data_type"] = constants.GET_LIST_WITH_COUNT
        family_list,total_count = db_helper.get_family_member(request)
        if not total_count:
            return Response(
                data=error_messages.DOCTOR_NOT_FOUND, status=status.HTTP_404_NOT_FOUND
            )
        serialize_data = PatientSerializer(user_obj,many=False).data
        serialize_data["family_members"] = AddFamilyMemberSerializer(family_list,many=True).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result=total_count if type(total_count) == int else None,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def update_family_detail(self,request):
    try:
        action_type = request.get("action_type",None)
        user_obj = request.get("user_master_obj")
        if user_obj.user_type.user_type_name.lower()!=constants.PATIENT:
            return Response(
                data=error_messages.INVALID_REQUEST, status=status.HTTP_412_PRECONDITION_FAILED
            )
        request["patient_obj"] = user_obj
        if action_type == constants.DELETE:
            family_list = db_helper.get_family_member(request)
            family_list.delete()
            return Response(data=error_messages.RECORD_DELETED,status=status.HTTP_200_OK)
        elif action_type == constants.UPDATE:
            family_member_id = request.get("family_member_id")
            if not family_member_id:
               return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
            family_obj,is_status = db_helper.get_family_member({
                "family_member_id":family_member_id,
                "data_type":constants.GET_FIRST_DATA
            })
            is_record_updated = AddFamilyMemberSerializer.update_record(self,request,family_obj)
            if is_record_updated:
               return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
        return Response(data=error_messages.INVALID_REQUEST,status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def manage_account(self,request):
    try:
        user_obj = request.get("user_master_obj")
        action_type = request.get("action_type",None)
        if user_obj.user_type.user_type_name.lower() !=constants.PATIENT:
            return Response(data=error_messages.INVALID_REQUEST,status=status.HTTP_412_PRECONDITION_FAILED)
        if not action_type:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        if action_type == constants.UPDATE:
            update_record = PatientSerializer.update_record(self,request,user_obj)
            if update_record:
                return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
        elif action_type == constants.DELETE:
            user_obj.delete()
            return Response(data=error_messages.ACCOUNT_DELETED,status=status.HTTP_200_OK)
        return Response(data=error_messages.INVALID_REQUEST,status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)


