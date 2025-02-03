import requests
from rest_framework import status
from rest_framework.response import Response
from healthcare.utils import shared,error_messages,db_helper,constants,logging_utils
from healthcare.doctor.serializers import (DoctorSerializer,DoctorStaffManagementSerializer,MedicineSerializer,
        PrescriptionSerializer,PrescriptionMedicineDetailserializer,PrescriptionTestDetailsSerializer)
from healthcare.models.doctor_model import MedicineMaster,Prescription,TestMaster,PrescriptionMedicineDetails

from healthcare.patient.serializers import AppointmentMasterSerializer

def get_profile(self,request):
    try:
        user_obj = request.get("user_master_ob",None)
        if user_obj.user_type.user_type_name.lower() !=constants.DOCTOR:
            return Response(data=error_messages.INVALID_REQUEST,status=status.HTTP_412_PRECONDITION_FAILED)
        serialize_data = DoctorSerializer(user_obj,many=False).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result = None,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
        
    except Exception as ex:
        logging_utils.logger_info(f"helper=doctor_helper, class=get_profile, exception={ex}")
        return logging_utils.main_exception(self.get_view_name(), ex)
    
def get_appointment(self,request):
    try:
        appointment_code = request.get("appointment_code",None)
        request['data_type'] = constants.GET_LIST_WITH_COUNT
        if appointment_code:
            request["data_type"] = constants.GET_FIRST_DATA
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def create_appointment(self,request):
    try:
        user_obj = request.get("user_master_obj",None)
        if user_obj.user_type.user_type_name.lower()!=constants.DOCTOR:
            return Response(
                data=error_messages.UNAUTHORIZE, status=status.HTTP_412_PRECONDITION_FAILED
            )
        patient_id = request.get("patient_id",None)
        if not patient_id:
            return Response(
                data=error_messages.PATIENT_DETAIL_NOT_PROVIDED, status=status.HTTP_412_PRECONDITION_FAILED
            )
        patient_obj,is_status = db_helper.get_user_master_data({"user_master_id":patient_id,"user_type_id":3,"data_type":constants.GET_FIRST_DATA})
        if not patient_obj:
            return Response(
                data=error_messages.PATIENT_NOT_FOUND, status=status.HTTP_404_NOT_FOUND
            )
        request["doctor_obj"] = user_obj
        request["patient_obj"] = patient_obj
        is_created = AppointmentMasterSerializer.insert(self,request)
        if is_created:
            return Response(
                data=error_messages.APPOINTMENT_CREATED, status=status.HTTP_200_OK
            )
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

def add_staff(self,request):
    try:
        mobile_number = request.get("mobile_number",None)
        email_id = request.get("email_id",None)
        user_obj = request.get("user_master_obj",None)
        user_type = request.get("user_type",None)

        if user_obj.user_type.user_type_name.lower() != constants.DOCTOR:
            return Response(data=error_messages.UNAUTHORIZE_FOR_ADDING_STAFF, status=status.HTTP_401_UNAUTHORIZED)
        if not user_type:
           return Response(data=error_messages.USER_TYPE_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        user_type_obj = db_helper.get_user_type({"user_type":user_type})
        if not user_type_obj:
            return Response(data=error_messages.INVALID_USER_TYPE,status=status.HTTP_412_PRECONDITION_FAILED)
        if mobile_number or email_id:
            if email_id:
                verify_email_id = shared.email_id_regex(email_id)
                if not verify_email_id:
                   return Response(data=error_messages.INVALID_EMAIL_ID,status=status.HTTP_412_PRECONDITION_FAILED)
                is_exist = db_helper.get_user_master_data({"email_id":email_id})
                if is_exist:
                   return Response(data=error_messages.EMAIL_EXISTS,status=status.HTTP_412_PRECONDITION_FAILED)
            if mobile_number:
                verify_mobile_no = shared.mobile_validator(mobile_number)
                if not verify_mobile_no:
                   return Response(data=error_messages.INVALID_EMAIL_ID,status=status.HTTP_412_PRECONDITION_FAILED)
                is_exist = db_helper.get_user_master_data({
                    "mobile_number":mobile_number
                })
                if is_exist:
                   return Response(data=error_messages.MOBILE_NO_EXISTS,status=status.HTTP_412_PRECONDITION_FAILED)
            request["doctor_obj"] = user_obj
            request["user_type_obj"] = user_type_obj
            is_added_staff = DoctorStaffManagementSerializer.insert(self,request)
            if is_added_staff:
               return Response(data=error_messages.STAFF_ACCOUNT_CREATED,status=status.HTTP_412_PRECONDITION_FAILED)
        return Response(data=error_messages.INVALID_REQUEST,status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def get_staff(self,request):
    try:
        doctor_obj = request.get("user_master_obj",None)
        if doctor_obj.user_type.user_type_name.lower()!=constants.DOCTOR:
            return Response(data=error_messages.UNAUTHORIZE_FOR_SEE_STAFF_RECORDS,status=status.HTTP_401_UNAUTHORIZED)
        request["doctor_obj"] = doctor_obj
        request["user_type_id"] = 4
        request["data_type"] = constants.GET_LIST_WITH_COUNT
        staff_list,total_count = db_helper.get_user_master_data(request)
        if not total_count:
           return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        serialize_data = DoctorStaffManagementSerializer(staff_list,many=True).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result=total_count,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return logging_utils.main_exception(self.get_view_name(), ex)
        # return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def manage_staff(self,request):
    try:
        action_type = request.get("action_type",None)
        doctor_obj = request.get("user_master_obj",None)
        staff_id = request.get("staff_id",None)

        if not staff_id:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        staff_obj,is_status = db_helper.get_user_master_data({
            "staff_id":staff_id,"doctor_obj":doctor_obj,"data_type":constants.GET_FIRST_DATA
        })
        if not staff_obj:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        if action_type == constants.UPDATE:
            if doctor_obj.user_type.user_type_name.lower() not in (constants.DOCTOR,constants.DOCTOR_STAFF):
               return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
            is_added_staff = DoctorStaffManagementSerializer.update_staff_record(self,request,staff_obj)
            if is_added_staff:
               return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
        elif action_type == constants.DELETE:
            if doctor_obj.user_type.user_type_name.lower() !=constants.DOCTOR:
               return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
            request["doctor_obj"]
            request["user_type_id"] = 4
            staff_list = db_helper.get_user_master_data(request)
            if not staff_list:
               return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            staff_list.delete()
            return Response(data=error_messages.RECORD_DELETED,status=status.HTTP_200_OK)
        return Response(data=error_messages.INVALID_REQUEST,status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def add_medicine(self,request):
    try:
        user_obj = request.get("user_master_obj",None)
        if user_obj.user_type.user_type_name.lower() not in (constants.DOCTOR,constants.DOCTOR_STAFF):
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        request["added_by"] = user_obj
        is_medicine_added = MedicineSerializer.insert(self,request)
        if is_medicine_added:
           return Response(data=error_messages.DATA_INSERTED,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def get_medicine(self,request):
    try:
        user_obj = request.get("user_master_obj",None)
        if user_obj.user_type.user_type_name.lower() not in (constants.DOCTOR,constants.DOCTOR_STAFF):
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        request["data_type"] = constants.GET_LIST_WITH_COUNT
        medicine_lst,total_count = db_helper.get_medicine_record(request)
        if not total_count:
           return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        serialize_data = MedicineSerializer(medicine_lst,many=True).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result=total_count,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def manage_medicine(self,request):
    try:
        action_type = request.get("action_type",None)
        user_obj = request.get("user_master_obj",None)
        medicine_id = request.get("medicine_id",None)
        medicine_id = request.get("medicine_id",None)
        if user_obj.user_type.user_type_name.lower() not in (constants.DOCTOR,):
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        if not medicine_id:
               return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        if not action_type:
           return Response(data=error_messages.ACTION_TYPE_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        if action_type == constants.DELETE:
            medicine_lst = db_helper.get_medicine_record(request)
            if not medicine_lst:
               return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            medicine_lst.delete()
            return Response(data=error_messages.RECORD_DELETED,status=status.HTTP_200_OK)
        request["updated_by"] = user_obj
        if action_type == constants.UPDATE:
            medicine_obj,is_status = db_helper.get_medicine_record({
                "medicine_id":medicine_id,
                "data_type":constants.GET_FIRST_DATA
            })
            if not is_status:
               return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
            is_medicine_updated = MedicineSerializer.updated_medicine(self,request,medicine_obj)
            if is_medicine_updated:
               return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
        return Response(data=error_messages.INVALID_REQUEST,status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    

def create_prescription(self,request):
    try:
        user_obj = request.get("user_master_obj",None)
        patient_id = request.get("patient_id",None)
        update_patient_detail = request.get("update_patient_detail",None)
        file = request.get("file",None)
        patient_obj = None
        doctor_obj = None
        if user_obj.user_type.user_type_name.lower() not in (constants.DOCTOR_STAFF,constants.DOCTOR):
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_412_PRECONDITION_FAILED)

        if user_obj.user_type.user_type_name.lower() == constants.DOCTOR_STAFF:
            doctor_id = user_obj.doctor_id
            doctor_obj = db_helper.get_user_master_data({
                "user_master_id":doctor_id,"user_type_id":2,"data_type":constants.GET_FIRST_DATA
            })
            if not doctor_obj:
                return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_412_PRECONDITION_FAILED)
            request["doctor_obj"] = doctor_obj
        else:
            doctor_obj = user_obj
            request["doctor_obj"] = doctor_obj
        if update_patient_detail:
            import json
            update_patient_detail = json.loads(update_patient_detail)
            if not update_patient_detail.get("patient_id"):
               return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
            patient_obj,is_status = db_helper.get_user_master_data({
                "user_master_id": update_patient_detail.get("patient_id"),"user_type_id":3,"data_type":constants.GET_FIRST_DATA
                })
            if not patient_obj:
               return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_412_PRECONDITION_FAILED)
            patient_id = patient_obj.id
            if update_patient_detail.get("patient_gender",None):
                patient_obj.gender = update_patient_detail.get("patient_gender")
            if update_patient_detail.get("patient_first_name",None):
                patient_obj.first_name = update_patient_detail.get("patient_first_name")
            if update_patient_detail.get("patient_last_name",None):
                patient_obj.last_name = update_patient_detail.get("patient_last_name")
            if update_patient_detail.get("patient_full_name",None):
                patient_obj.full_name = update_patient_detail.get("patient_full_name")
            if update_patient_detail.get("patient_age",None):
                patient_obj.age = update_patient_detail.get("patient_age")
            if update_patient_detail.get("patient_email",None):
                patient_obj.email = update_patient_detail.get("patient_email")
            patient_obj.save()
        if not patient_id:
            return Response(data=error_messages.DATA_NOT_PROVIDED,status=status.HTTP_412_PRECONDITION_FAILED)
        if not patient_obj:
           patient_obj,is_status = db_helper.get_user_master_data({
               "user_master_id": patient_id,"data_type":constants.GET_FIRST_DATA
               })
        if not patient_obj:
            return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_412_PRECONDITION_FAILED)
        request["added_by"] = user_obj
        request["patient_obj"] = patient_obj
        is_prescription_added = PrescriptionSerializer.insert(self,request)
        if is_prescription_added:
           is_prescription_medicine_detail_added = PrescriptionMedicineDetailserializer.insert(self,request,is_prescription_added)
           is_prescription_test_detail_added = PrescriptionTestDetailsSerializer.insert(self,request,is_prescription_added)
           if file:
                body = '''\
                <html>
                <head></head>
                <body>
                    <p>
                        Dear Sir,<br><br><br>
                        <b>'''+f'Please find your prescription pdf file'+'''</b><br><br>
                        Medical Services.
                    </p>
                </body>
                </html>
               '''
                file = file.read()
                if patient_obj.email_id:
                  shared.send_email("prescription pdf file",body,patient_obj.email_id,file)
                if doctor_obj.email_id:
                  shared.send_email("prescription pdf file",body,doctor_obj.email_id,file)
           return Response(data=error_messages.DATA_INSERTED,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def get_prescription(self,request):
    try:
        user_obj, is_status = db_helper.get_user_master_data({
            "user":request.get("user"),
            "data_type":constants.GET_FIRST_DATA
            })
        if user_obj.user_type.user_type_name.lower() not in (constants.DOCTOR,constants.DOCTOR_STAFF):
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        request["data_type"] = constants.GET_LIST_WITH_COUNT
        medicine_lst,total_count = db_helper.get_prescription_record(request)
        if not total_count:
           return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        serialize_data = MedicineSerializer(medicine_lst,many=True).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result=total_count,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def manage_prescripton(self,request):
    try:
        action_type = request.get("action_type",None)
        user_obj = db_helper.get_user_master_data({
            "user":request.get("user"),
            "data_type":constants.GET_FIRST_DATA
            })
        if user_obj.user_type.user_type_name.lower() not in (constants.DOCTOR,constants.DOCTOR_STAFF):
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        prescription_lst,total_count = db_helper.get_prescription_record(request)
        if not total_count:
           return Response(data=error_messages.DATA_NOT_FOUND,status=status.HTTP_404_NOT_FOUND)
        request["updated_by"] = user_obj
        if action_type == constants.UPDATE:
            prescription_obj = prescription_lst.first()
            is_prescription_updated = PrescriptionSerializer.update_prescription(self,request,prescription_obj)
            return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
        if action_type == constants.DELETE:
            prescription_lst.delete()
            return Response(data=error_messages.RECORD_DELETED,status=status.HTTP_200_OK)
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
            update_record = DoctorSerializer.update_record(self,request,user_obj)
            if update_record:
                return Response(data=error_messages.DATA_UPDATED,status=status.HTTP_200_OK)
        elif action_type == constants.UPDATE:
            user_obj.delete()
            return Response(data=error_messages.ACCOUNT_DELETED,status=status.HTTP_200_OK)
        return Response(data=error_messages.INVALID_REQUEST,status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
    
def get_staff_profile(self,request):
    try:
        user_obj = request.get("user_master_obj")

        if user_obj.user_type.user_type_name.lower() !=constants.DOCTOR_STAFF:
            return Response(data=error_messages.UNAUTHORIZE,status=status.HTTP_401_UNAUTHORIZED)
        serialize_data = DoctorStaffManagementSerializer(user_obj,many=False).data
        translator_response = shared.basic_response_translator(
            is_success=True,
            total_result = None,
            data=serialize_data
        )
        return Response(data=translator_response,status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)