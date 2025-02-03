import requests
from rest_framework import status
from rest_framework.response import Response
from healthcare.utils import shared,error_messages,db_helper,constants,logging_utils
from healthcare.doctor.serializers import DoctorSerializer,DoctorStaffManagementSerializer,MedicineSerializer,PrescriptionSerializer
from healthcare.patient.serializers import AppointmentMasterSerializer,PatientSerializer
from healthcare.medical_admin.serializers import SymptomMasterSerializer,SymptomDetailSerializer

def appointment_history(self,request):
    try:
        user_obj = request.get("user_master_obj",None),
        if user_obj.user_type.user_type_name.lower() !=constants.ADMIN:
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        appointment_lst,total_count = db_helper.get_appointment(request)
        if not total_count:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        serialize_data = AppointmentMasterSerializer(appointment_lst,many=True).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result=total_count if type(total_count) == int else None,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return False
    
def get_medicine(self,request):
    try:
        medicine_lst,total_count = db_helper.get_medicine_record(request)
        if not total_count:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        serialize_data = MedicineSerializer(medicine_lst,many=True).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result=total_count if type(total_count) == int else None,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return False
    
def manage_medicine(self,request):
    try:
        user_obj = request.get("user_master_obj",None)
        action_type = request.get("action_type",None)
        medicine_id = request.get("medicine_id",None)
        if user_obj.user_type.user_type_name.lower() !=constants.ADMIN:
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        if not action_type:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        if not medicine_id:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        medicine_obj,is_status = db_helper.get_medicine_record({"medicine_id":medicine_id,"data_type":constants.GET_FIRST_DATA})
        if not is_status:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        if action_type == constants.UPDATE:
            is_updated = MedicineSerializer.updated_medicine(self,request,medicine_obj)
            if is_updated:
               return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
        elif action_type == constants.DELETE:
            medicine_obj.delete()        
    except Exception as ex:
        return logging_utils.main_exception(self.get_view_name(), ex)
    
def manage_doctor(self,request):
    try:
        user_obj = request.get("user_master_obj",None)
        action_type = request.get("action_type",None)
        doctor_id = request.get("doctor_id",None)
        if user_obj.user_type.user_type_name.lower() !=constants.ADMIN:
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        if not action_type:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        if not doctor_id:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        doctor_obj,is_status = db_helper.get_user_master_data({"doctor_id":doctor_id,"data_type":constants.GET_FIRST_DATA})
        if not is_status:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        if action_type == constants.UPDATE:
            is_updated = DoctorSerializer.update_record(self,request,doctor_obj)
            if is_updated:
               return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
        elif action_type == constants.DELETE:
            doctor_obj.delete()        
    except Exception as ex:
        return logging_utils.main_exception(self.get_view_name(), ex)
    
def get_doctor(self,request):
    try:
        medicine_lst,total_count = db_helper.UserType(request)
        if not total_count:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        serialize_data = MedicineSerializer(medicine_lst,many=True).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result=total_count if type(total_count) == int else None,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return logging_utils.main_exception(self.get_view_name(), ex)

def manage_patient(self,request):
    try:
        user_obj = request.get("user_master_obj",None)
        action_type = request.get("action_type",None)
        manage_patient = request.get("manage_patient",None)
        if user_obj.user_type.user_type_name.lower() !=constants.ADMIN:
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        if not action_type:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        if not manage_patient:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        patient_obj,is_status = db_helper.get_user_master_data({"patient_id":manage_patient,"data_type":constants.GET_FIRST_DATA})
        if not is_status:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        if action_type == constants.UPDATE:
            is_updated = PatientSerializer.update_record(self,request,patient_obj)
            if is_updated:
               return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
        elif action_type == constants.DELETE:
            patient_obj.delete()        
    except Exception as ex:
        return logging_utils.main_exception(self.get_view_name(), ex)
    
def add_symptoms(self,request):
    try:
        user_obj = request.get("user_master_obj",None)
        symptom_detail_name_list = request.get("symptom_detail_name_list",[])
        body_part_name = request.get("body_part_name",None)
        already_exists_symptom_list = None
        if user_obj.user_type.user_type_name.lower() !=constants.ADMIN:
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        if not symptom_detail_name_list:
               return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        if not body_part_name:
               return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        symptom_master_obj,is_status = db_helper.get_symptom_master_data({
            "body_part_name":body_part_name,"data_type":constants.GET_FIRST_DATA
            })
        if not is_status:
           symptom_master_obj = SymptomMasterSerializer.insert(self,request)
        symptom_detail_obj_list = db_helper.get_symptom_detail_data({"symptom_detail_name_list":symptom_detail_name_list})
        if symptom_detail_obj_list:
            already_exists_symptom_list = symptom_detail_obj_list.values_list('name', flat=True)
            symptom_detail_name_list = list(set(symptom_detail_name_list) - set(already_exists_symptom_list.values_list('name', flat=True)))
        if symptom_detail_name_list:
            request["symptom_detail_name_list"] = symptom_detail_name_list
            is_created = SymptomDetailSerializer.insert(self,request,symptom_master_obj)
            if is_created:
                msg = {
                'success': True,
                'data': {
                    'message': 'Data Saved successfully',
                    'data_saved_list': symptom_detail_name_list,
                    'already_exists_symptom_list': already_exists_symptom_list
                }
            }
                return Response(data=msg,status=status.HTTP_200_OK)
        else:
            msg = {
                'success': False,
                'data': {
                    'message': 'symptom already exists',
                    'already_exists_symptom_list': already_exists_symptom_list
                }
            }
            return Response(data=msg,status=status.HTTP_409_CONFLICT)
    except Exception as ex:
        logging_utils.logger_info(f"helper=admin_helper, func=add_symptoms, exception={ex}")
        return logging_utils.main_exception(self.get_view_name(), ex)
    
def get_symptoms(self,request):
    try:
        user_obj = request.get("user_master_obj",None)
        action_type = request.get("action_type",None)
        symptom_id = request.get("symptom_id",None)
        if user_obj.user_type.user_type_name.lower() !=constants.ADMIN:
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
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
        elif action_type == constants.DETAIL_DATA:
            if not symptom_id:
               return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
            request["data_type"] = constants.GET_LIST_WITH_COUNT
            records,total_count = db_helper.get_symptom_detail_data(request)
            if total_count:
                serialize_data = SymptomMasterSerializer(records,many=True).data
                if serialize_data:
                    translator_response = shared.basic_response_translator(
                        is_success=True,
                        total_result=total_count,
                        data=records
                    )
                    return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        logging_utils.logger_info(f"helper=admin_helper, func=get_symptoms, exception={ex}")
        return logging_utils.main_exception(self.get_view_name(), ex)
    
def manage_symptoms(self, request):
    try:
        user_obj = request.get("user_master_obj",None)
        action_type = request.get("action_type",None)
        symptom_id = request.get("symptom_id")
        if user_obj.user_type.user_type_name.lower() !=constants.ADMIN:
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        if not action_type:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        if not symptom_id:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        medicine_obj,is_status = db_helper.get_symtom_master_data({"symptom_id":symptom_id,"data_type":constants.GET_FIRST_DATA})
        if not is_status:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        if action_type == constants.UPDATE:
            is_updated = SymptomMasterSerializer.updated_medicine(self,request,medicine_obj)
            if is_updated:
               return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
        elif action_type == constants.DELETE:
            medicine_obj.delete() 
    except Exception as ex:
        logging_utils.logger_info(f"helper=admin_helper, class=manage_symptoms, exception={ex}")
        return logging_utils.main_exception(self.get_view_name(), ex)