from healthcare.models.master_model import (OTPGenerator,User,UserType,
    PasswordMaster,CronScriptLock,SymptomMaster,SymptomDetails,TransactionMaster, User)
from healthcare.models.patient_model import AppointmentMaster,PatientFamilyDetails,AppointmentDetails
from healthcare.utils import constants,error_messages,logging_utils
from rest_framework.response import Response
from rest_framework import status
from healthcare.models.doctor_model import MedicineMaster,Prescription,TestMaster
from django.utils import timezone

def get_otp(request):
    try:
        kwargs = {}
        otp_number = request.get('otp_number', None)
        phone_number = request.get('phone_number', None)
        offset = request.get('offset', 0)
        limit = request.get('limit', 5)
        data_type = request.get('data_type', None)
        if otp_number:
            kwargs["otp_number"] = otp_number
        if phone_number:
            kwargs["phone_number"] = phone_number
        records = OTPGenerator.objects.filter(
            **kwargs
        ).order_by('-id')
        return records
    except Exception as ex:
        Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

    
def get_user_type(request):
    try:
        kwargs = {}
        user_type = request.get("user_type",None)

        if user_type:
            kwargs["user_type_name__iexact"] = user_type
        return UserType.objects.filter(**kwargs).first()
    except Exception as ex:
        Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

    
def get_user_master_data(request):
    try:
        kwargs = {}
        mobile_number = request.get("mobile_number",None)
        gender = request.get("gender",None)
        user_type_id = request.get("user_type_id",None)
        user_type_obj = request.get("user_type_obj",None)
        doctor_obj = request.get("doctor_obj",None)  # This filter is require for get doctor staff records
        is_user = request.get("user",None)    # This filter is using in the function get_request_data which is in shared
        user_master_id = request.get("user_master_id",None)
        email_id = request.get("email_id",None)
        experience = request.get("experience",None)
        city = request.get("city",None)
        pincode = request.get("pincode",None)
        state = request.get("state",None)
        speciality = request.get("speciality",None)
        data_type = request.get("data_type",None)
        offset = request.get("offset",0)
        limit = request.get("limit",20)

        if user_master_id:
            kwargs["id"] = user_master_id
        if mobile_number:
            kwargs["mobile_number"] = mobile_number
        if user_type_obj:
            kwargs["user_type"] = user_type_obj
        if is_user:
            kwargs["user"] = is_user
        if gender:
            kwargs["gender"] = gender
        if user_type_id:
            kwargs["user_type_id"] = user_type_id
        if experience:
            kwargs["experience"] = experience
        if city:
            kwargs["city"] = city
        if pincode:
            kwargs["pincode"] = pincode
        if state:
            kwargs["state"] = state
        if speciality:
            kwargs["speciality"] = speciality
        if email_id:
            kwargs["email_id__iexact"] = email_id
        if doctor_obj:
            kwargs["doctor"] = doctor_obj

        if data_type == constants.GET_FIRST_DATA:
           user_obj = User.objects.filter(**kwargs).first()
           return user_obj,bool(user_obj)
        if data_type == constants.GET_LIST_WITH_COUNT:
           user_obj_lst = User.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
           total_count = User.objects.filter(**kwargs).count()
           return user_obj_lst,total_count
        user_obj_lst = User.objects.filter(**kwargs).order_by("-id")
        return user_obj_lst
    except Exception as ex:
        logging_utils.helper_error(view="db_helper", function_name="get_user_master_data", exception=str(ex))
        Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

    
def get_user_password(request):
    try:
      if request.get("user_obj"):
        return PasswordMaster.objects.filter(user_master = request.get("user_obj")).first()
      obj,created = PasswordMaster.objects.get_or_create(user_master = request.get("user_master"))
      return obj,created
    except Exception as ex:
        Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

    
def get_appointment(request):
    try:
        kwargs = {}
        patient_obj = request.get("patient_obj",None)
        doctor_obj = request.get("doctor_obj",None)
        date = request.get("date",None)
        from_date = request.get("from_date",None)
        to_date = request.get("to_date",None)
        from_time = request.get("from_time",None)
        to_time = request.get("to_time",None)
        current_time = request.get("current_time",None)
        appointment_id = request.get("appointment_id",None)
        appointment_code = request.get("appointment_code",None)
        appointment_type = request.get("appointment_type",None)
        symptoms = request.get("symptoms",None)
        is_active = request.get("is_active",None)
        time_slot_from = request.get("time_slot_from",None)
        time_slot_to = request.get("time_slot_to",None)
        #   added_by = request.get("user_master_obj",None)
        data_type = request.get("data_type",None)
        offset = request.get("offset",0)
        limit = request.get("limit",20)
        
        if patient_obj:
            kwargs["patient"] = patient_obj
        if appointment_id:
            kwargs["id"] = appointment_id
        if doctor_obj:
            kwargs["doctor"] = doctor_obj
        if date:
            kwargs["date"] = date
        if from_date:
            kwargs["date__gte"] = from_date
        if to_date:
            kwargs["date__lte"] = to_date
        if from_time:
            kwargs["time_slot_to__gte"] = from_time
        if to_time:
            kwargs["time_slot_to__lte"] = to_time
        if current_time:
            kwargs["time_slot_to__lt"] = current_time
        if appointment_code:
            kwargs["appointment_code"] = appointment_code
        if appointment_type:
            kwargs["appointment_type__iexact"] = appointment_type
        if symptoms:
            kwargs["symptoms__icontains"] = symptoms
        if time_slot_from:
            kwargs["time_slot_from__gte"] = time_slot_from
        if time_slot_to:
            kwargs["time_slot_to__lte"] = time_slot_to
        #   if added_by:
        #     kwargs["added_by"] = added_by
        
        if is_active:
            if is_active == constants.ACTIVE:
                    kwargs["is_active"] = True
            elif is_active == constants.IN_ACTIVE:
                    kwargs["is_active"] = False

        if data_type == constants.GET_FIRST_DATA:
            appointment_obj = AppointmentMaster.objects.filter(**kwargs).first()
            return appointment_obj,bool(appointment_obj)
        if data_type == constants.GET_LIST_WITH_COUNT:
            appointment_lst = AppointmentMaster.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
            total_count = AppointmentMaster.objects.filter(**kwargs).count()
            return appointment_lst,total_count
        appointment_lst = AppointmentMaster.objects.filter(**kwargs).order_by("-id")
        return appointment_lst
    except Exception as ex:
        logging_utils.logger_info(str(ex))
        return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

    
def get_staff_list(request):
   try:
        kwargs = {}
        mobile_number = request.get("mobile_number",None)
        gender = request.get("gender",None)
        user_type_id = request.get("user_type_id",None)
        user_type_obj = request.get("user_type_obj",None)
        is_user = request.get("user",None)
        user_master_id = request.get("user_master_id",None)
        doctor = request.get("doctor",None)
        patient = request.get("patient",None)
        user_obj = request.get("user_obj",None)
        email_id = request.get("email_id",None)
        experience = request.get("experience",None)
        city = request.get("city",None)
        pincode = request.get("pincode",None)
        state = request.get("state",None)
        speciality = request.get("speciality",None)
        data_type = request.get("data_type",None)
        offset = request.get("offset",0)
        limit = request.get("limit",20)

        if user_master_id:
            kwargs["id"] = user_master_id
        if doctor:
            kwargs["id"] = doctor
        if patient:
            kwargs["id"] = patient
        if mobile_number:
            kwargs["mobile_number"] = mobile_number
        if user_type_obj:
            kwargs["user_type"] = user_type_obj
        if is_user:
            kwargs["user"] = is_user
        if gender:
            kwargs["gender"] = gender
        if user_type_id:
            kwargs["user_type_id"] = user_type_id
        if experience:
            kwargs["experience"] = experience
        if city:
            kwargs["city"] = city
        if pincode:
            kwargs["pincode"] = pincode
        if state:
            kwargs["state"] = state
        if speciality:
            kwargs["speciality"] = speciality
        if email_id:
            kwargs["email_id"] = email_id
        
        if data_type == constants.GET_FIRST_DATA:
           user_obj = User.objects.filter(**kwargs).first()
           return user_obj,bool(user_obj)
        if data_type == constants.GET_LIST_WITH_COUNT:
           user_obj = User.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
           total_count = User.objects.filter(**kwargs).count()
           return user_obj,total_count
        user_obj = User.objects.filter(**kwargs).order_by("-id")
        return user_obj
   except Exception as ex:
      Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

def get_medicine_record(request):
    try:
        kwargs = {}
        drug = request.get("drug",None)
        strength = request.get("strength",None)
        medicine_id = request.get("medicine_id",None)
        medicine_name = request.get("medicine_name",None)
        medicine_type = request.get("medicine_type",None)
        cost_of_medicine = request.get("cost_of_medicine",None)
        purpose = request.get("purpose",None)
        medicine_desc = request.get("medicine_desc",None)
        manufacturer = request.get("manufacturer",None)
        acronym = request.get("acronym",None)
        # updated_by = request.get("updated_by",None)
        data_type = request.get("data_type",None)
        offset = request.get("offset",0)
        limit = request.get("limit",20)
        
        if medicine_id:
            kwargs["id"] = medicine_id
        if drug:
            kwargs["drug"] = drug
        if strength:
            kwargs["strength"] = strength
        if medicine_name:
            kwargs["medicine_name"] = medicine_name
        if medicine_type:
            kwargs["medicine_type"] = medicine_type
        if cost_of_medicine:
            kwargs["cost_of_medicine"] = cost_of_medicine
        if purpose:
            kwargs["purpose"] = purpose
        if medicine_desc:
            kwargs["medicine_desc"] = medicine_desc
        if manufacturer:
            kwargs["medicine_desc"] = manufacturer
        if acronym:
            kwargs["acronym"] = acronym
        # if updated_by:
        #     kwargs["updated_by"] = updated_by
            
        if data_type == constants.GET_FIRST_DATA:
           medicine_obj = MedicineMaster.objects.filter(**kwargs).first()
           return medicine_obj,bool(medicine_obj)
        if data_type == constants.GET_LIST_WITH_COUNT:
           medicine_obj = MedicineMaster.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
           total_count = MedicineMaster.objects.filter(**kwargs).count()
           return medicine_obj,total_count
        medicine_obj = MedicineMaster.objects.filter(**kwargs).order_by("-id")
        return medicine_obj
    except Exception as ex:
      Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

def get_family_member(request):
    try:
        kwargs = {}
        mobile_number = request.get("mobile_number",None)
        gender = request.get("gender",None)
        patient_obj = request.get("patient_obj",None)
        family_member_id = request.get("family_member_id",None)
        email_id = request.get("email_id",None)
        experience = request.get("experience",None)
        city = request.get("city",None)
        pincode = request.get("pincode",None)
        state = request.get("state",None)
        full_name = request.get("full_name",None)
        first_name = request.get("first_name",None)
        last_name = request.get("last_name",None)
        data_type = request.get("data_type",None)
        is_active = request.get("is_active",None)
        offset = request.get("offset",0)
        limit = request.get("limit",20)

        if patient_obj:
            kwargs["patient"] = patient_obj
        if full_name:
            kwargs["full_name"] = full_name
        if first_name:
            kwargs["first_name"] = first_name
        if last_name:
            kwargs["last_name"] = last_name
        if mobile_number:
            kwargs["mobile_number"] = mobile_number
        if gender:
            kwargs["gender"] = gender
        if experience:
            kwargs["experience"] = experience
        if city:
            kwargs["city"] = city
        if pincode:
            kwargs["pincode"] = pincode
        if state:
            kwargs["state"] = state
        if email_id:
            kwargs["email_id__iexact"] = email_id
        if family_member_id:
            kwargs["id"] = family_member_id

        if is_active:
            if is_active == constants.ACTIVE:
                kwargs["is_active"] = True
            elif is_active == constants.IN_ACTIVE:
                kwargs["is_active"] = False
        
        if data_type == constants.GET_FIRST_DATA:
           user_obj = PatientFamilyDetails.objects.filter(**kwargs).first()
           return user_obj,bool(user_obj)
        if data_type == constants.GET_LIST_WITH_COUNT:
           user_obj = PatientFamilyDetails.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
           total_count = PatientFamilyDetails.objects.filter(**kwargs).count()
           return user_obj,total_count
        user_obj = PatientFamilyDetails.objects.filter(**kwargs).order_by("-id")
        return user_obj
    except Exception as ex:
      Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

def get_prescription_data(request):
    try:
        kwargs = {}
        doctor_obj = request.get("doctor_obj",None)
        doctor_id = request.get("doctor_id",None)
        patient_obj = request.get("patient_obj",None)
        medicine_recomended_from_inside = request.get("medicine_recomended_from_inside",None)
        medicine_recomended_from_outside = request.get("medicine_recomended_from_outside",None)
        advice = request.get("advice",None)
        test_advice = request.get("test_advice",None)
        other_advice = request.get("other_advice",None)
        next_consult = request.get("next_consult",None)
        data_type = request.get("data_type",None)
        offset = request.get("offset",0)
        limit = request.get("limit",20)

        if doctor_obj:
            kwargs["doctor"] = doctor_obj
        if doctor_id:
            kwargs["doctor__id"] = doctor_id
        if patient_obj:
            kwargs["patient"] = patient_obj
        if medicine_recomended_from_inside:
            kwargs["medicine_recomended_from_inside"] = medicine_recomended_from_inside
        if medicine_recomended_from_outside:
            kwargs["medicine_recomended_from_outside"] = medicine_recomended_from_outside
        if advice:
            kwargs["advice"] = advice
        if test_advice:
            kwargs["test_advice"] = test_advice
        if other_advice:
            kwargs["other_advice"] = other_advice
        if next_consult:
            kwargs["next_consult"] = next_consult
        if data_type == constants.GET_FIRST_DATA:
           prescrip_obj = Prescription.objects.filter(**kwargs).first()
           return prescrip_obj,bool(prescrip_obj)
        if data_type == constants.GET_LIST_WITH_COUNT:
           prescrip_obj = Prescription.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
           total_count = Prescription.objects.filter(**kwargs).count()
           return prescrip_obj,total_count
        prescrip_obj = Prescription.objects.filter(**kwargs).order_by("-id")
        return prescrip_obj
    except Exception as ex:
      Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

def update_cron_status_one_time_cron(cron_script_obj, status):
    try:
        if status == CronScriptLock.RUNNING:
            cron_script_obj.one_time_cron_status = CronScriptLock.RUNNING
            cron_script_obj.one_time_cron_started_dt = timezone.now()
            cron_script_obj.save()
        elif status == CronScriptLock.STOPPED:
            cron_script_obj.one_time_cron_status = CronScriptLock.STOPPED
            cron_script_obj.one_time_cron_ended_dt = timezone.now()
            cron_script_obj.data_from_date = None
            cron_script_obj.is_one_time_cron = False
            cron_script_obj.save()
        return True

    except Exception as ex:
        return False

def update_cron_status_regular_cron(cron_script_obj, status):
    try:
        if status == CronScriptLock.RUNNING:
            cron_script_obj.regular_cron_status = CronScriptLock.RUNNING
            cron_script_obj.regular_cron_started_dt = timezone.now()
            cron_script_obj.save()
        elif status == CronScriptLock.STOPPED:
            cron_script_obj.regular_cron_status = CronScriptLock.STOPPED
            cron_script_obj.regular_cron_ended_dt = timezone.now()
            cron_script_obj.save()
        return True
    except Exception as ex:
        return False

def check_cron_date(cron_script_obj):
    try:
        get_difference = timezone.now() - cron_script_obj.regular_cron_started_dt
        seconds = get_difference.seconds
        if seconds <= 18000:
            return False
        update_cron_status_regular_cron(cron_script_obj, CronScriptLock.STOPPED)
        return True
    except Exception as ex:
        return False
    
def check_script_log(cron_name):
    try:
        cronscriptlock_obj, created = CronScriptLock.objects.get_or_create(
            cron_script_name=cron_name,
            defaults={'is_one_time_cron': True, 'one_time_cron_status': "stopped",
                      'one_time_cron_started_dt': timezone.now(),
                      'one_time_cron_ended_dt': timezone.now(),
                      'regular_cron_status': "stopped",
                      'regular_cron_started_dt': timezone.now(),
                      'regular_cron_ended_dt': timezone.now()
                      }
        )
        return cronscriptlock_obj
    except Exception as ex:
        return False

def get_symptom_master_data(request):
    try:
        kwargs = {}
        symptom_id = request.get('symptom_id',None)
        body_part_name = request.get('body_part_name',None)
        data_type = request.get('data_type',None)
        is_active = request.get("is_active",None)
        offset = request.get("offset",0)
        limit = request.get("limit",20)


        if body_part_name:
            kwargs["body_part_name__iexact"] = body_part_name
        if symptom_id:
            kwargs["id"] = symptom_id
        
        if is_active:
            if is_active == constants.ACTIVE:
                kwargs["is_active"] = True
            elif is_active == constants.IN_ACTIVE:
                kwargs["is_active"] = False
        
        if data_type == constants.GET_FIRST_DATA:
           obj = SymptomMaster.objects.filter(**kwargs).first()
           return obj,bool(obj)
        if data_type == constants.GET_LIST_WITH_COUNT:
           obj = SymptomMaster.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
           total_count = SymptomMaster.objects.filter(**kwargs).count()
           return obj,total_count
        obj = SymptomMaster.objects.filter(**kwargs).order_by("-id")
        return obj
    except Exception as ex:
        return False
    
def get_symptom_detail_data(request):
    try:
        kwargs = {}
        symptom_name = request.get('symptom_name',None)
        symptom_id = request.get('symptom_id',None)
        body_part_name = request.get('body_part_name',None)
        body_part_id = request.get('body_part_id',None)
        symptom_detail_id = request.get('symptom_detail_id',None)
        symptom_detail_name_list = request.get('symptom_detail_name_list',None)
        data_type = request.get('data_type',None)
        is_active = request.get("is_active",None)
        offset = request.get("offset",0)
        limit = request.get("limit",20)


        if body_part_id:
            kwargs["symptoms_id"] = body_part_id
        if body_part_name:
            kwargs["symptoms__body_part_name__iexact"] = body_part_name
        if symptom_name:
            kwargs["name"] = symptom_name
        if symptom_detail_name_list:
            kwargs["name__in"] = symptom_detail_name_list
        if symptom_id:
            kwargs["id"] = symptom_id
        if symptom_detail_id:
            kwargs["id"] = symptom_detail_id
        
        if is_active:
            if is_active == constants.ACTIVE:
                kwargs["is_active"] = True
            elif is_active == constants.IN_ACTIVE:
                kwargs["is_active"] = False
        
        if data_type == constants.GET_FIRST_DATA:
           obj = SymptomDetails.objects.filter(**kwargs).first()
           return obj,bool(obj)
        if data_type == constants.GET_LIST_WITH_COUNT:
           obj = SymptomDetails.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
           total_count = SymptomDetails.objects.filter(**kwargs).count()
           return obj,total_count
        obj = SymptomDetails.objects.filter(**kwargs).order_by("-id")
        return obj
    except Exception as ex:
        return False
    
def get_transaction_data(request):
    try:
        kwargs = {}
        transaction_id = request.get('transaction_id',None)
        appointment_id = request.get('appointment_id',None)
        razorpay_order_id = request.get('razorpay_order_id',None)
        data_type = request.get('data_type',None)
        is_active = request.get("is_active",None)
        is_paid = request.get("is_paid",None)
        offset = request.get("offset",0)
        limit = request.get("limit",20)
        if transaction_id:
            kwargs["id"] = transaction_id
        if appointment_id:
            kwargs["appointment_id"] = appointment_id
        if razorpay_order_id:
            kwargs["razorpay_order_id__iexact"] = razorpay_order_id
        if is_paid:
            if is_paid == constants.IN_ACTIVE:
               kwargs["is_paid"] = False
            elif is_paid == constants.IN_ACTIVE:
               kwargs["is_paid"] = True

        if data_type == constants.GET_FIRST_DATA:
           obj = TransactionMaster.objects.filter(**kwargs).first()
           return obj,bool(obj)
        if data_type == constants.GET_LIST_WITH_COUNT:
           obj = TransactionMaster.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
           total_count = TransactionMaster.objects.filter(**kwargs).count()
           return obj,total_count
        obj = TransactionMaster.objects.filter(**kwargs).order_by("-id")
        return obj
    except Exception as ex:
        return False    
    
def get_appointment_detail_data(request):
    try:
        kwargs = {}
        appointment_id = request.get('appointment_id',None)
        appointment_type = request.get('appointment_type',None)
        appointment_code = request.get('appointment_code',None)
        symptom_id = request.get('symptom_id',None)
        symptom_name = request.get('symptom_name',None)
        data_type = request.get('data_type',None)
        is_active = request.get("is_active",None)
        offset = request.get("offset",0)
        limit = request.get("limit",20)
        if appointment_id:
            kwargs["appointment_id"] = appointment_id
        if appointment_code:
            kwargs["appointment__appointment_code"] = appointment_code
        if appointment_type:
            kwargs["appointment__appointment_type"] = appointment_type
        if symptom_id:
            kwargs["symptom_id"] = symptom_id
        if symptom_name:
            kwargs["symptom__name"] = symptom_name

        if data_type == constants.GET_FIRST_DATA:
           obj = AppointmentDetails.objects.filter(**kwargs).first()
           return obj,bool(obj)
        if data_type == constants.GET_LIST_WITH_COUNT:
           obj = AppointmentDetails.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
           total_count = AppointmentDetails.objects.filter(**kwargs).count()
           return obj,total_count
        obj = AppointmentDetails.objects.filter(**kwargs).order_by("-id")
        return obj
    except Exception as ex:
        return False    
    
def get_test_master_data(request):
    try:
        kwargs = {}
        test_id = request.get('test_id',None)
        name = request.get('name',None)
        added_by = request.get('added_by',None)
        data_type = request.get('data_type',None)
        is_active = request.get("is_active",None)
        offset = request.get("offset",0)
        limit = request.get("limit",20)

        if test_id:
            kwargs["id"] = test_id
        if name:
            kwargs["name"] = name
        if added_by:
            kwargs["added_by"] = added_by
        
        if data_type == constants.GET_FIRST_DATA:
            obj = TestMaster.objects.filter(**kwargs).first()
            return obj,bool(obj)
        elif data_type == constants.GET_LIST_WITH_COUNT:
            obj = TestMaster.objects.filter(**kwargs).order_by("-id")[offset:offset+limit]
            total_count = TestMaster.objects.filter(**kwargs).count()
            return obj,total_count
        obj = TestMaster.objects.filter(**kwargs).order_by("-id")
        return obj
    except Exception as ex:
        logging_utils.helper_error("db_helper","get_test",ex)
        return False
        