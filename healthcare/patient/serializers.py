from rest_framework import serializers
from healthcare.models.master_model import UserMaster
from healthcare.models.patient_model import AppointmentMaster,PatientFamilyDetails,AppointmentDetails
from rest_framework.response import Response
from healthcare.utils import error_messages,shared,constants
from rest_framework import status
from datetime import datetime, time
import pandas as pd

class PatientSerializer(serializers.ModelSerializer):
    patient_id = serializers.CharField(source='id')
    user_type = serializers.CharField(source='user_type.user_type_name')
    class Meta:
        model = UserMaster
        fields = (
            'patient_id','first_name','last_name','email_id','full_name','user_type','mobile_number','address_1','address_2',
            'state','city','pincode','gender','occupation'
        )

    def update_record(self,request,obj):
        try:
            mobile_number = request.get("mobile_number",None)
            first_name = request.get("first_name",None)
            last_name = request.get("last_name",None)
            address_1 = request.get("address_1",None)
            address_2 = request.get("address_2",None)
            city = request.get("city",None)
            state = request.get("state",None)
            pincode = request.get("pincode",None)
            age = request.get("age",None)
            dob = request.get("dob",None)
            email_id = request.get("email_id",None)
            country = request.get("country",None)
            qualification = request.get("qualification",None)
            occupation = request.get("occupation",None)
            full_name = request.get("full_name",None)
            gender = request.get("gender",None)
            user_master_obj = request.get("user_master_obj",None)
            is_verified = request.get("is_verified",None)
            
            if mobile_number:
                obj.mobile_number = mobile_number
            if first_name:
                obj.first_name = first_name 
            if last_name:
                obj.last_name = last_name 
            if address_1:
                obj.address_1 = address_1 
            if address_2:
                obj.address_2 = address_2 
            if city:
                obj.city = city 
            if state:
                obj.state = state 
            if pincode:
                obj.pincode = pincode 
            if age:
                obj.age = age 
            if dob:
                obj.dob = dob 
            if email_id:
                obj.email_id = email_id 
            if country:
                obj.country = country 
            if qualification:
               obj.qualification = qualification 
            if full_name:
                obj.full_name = full_name 
            if gender:
                obj.gender = gender 
            if occupation:
                obj.occupation = occupation
            if user_master_obj.user_type.user_type_name.lower() !=constants.ADMIN:
                if is_verified == constants.ACTIVE:
                    obj.is_verified = True
                elif is_verified == constants.IN_ACTIVE:
                    obj.is_verified = False
                obj.verified_by = user_master_obj
            obj.save()
            return True
        except Exception as ex:
            return False

class AppointmentMasterSerializer(serializers.ModelSerializer):
    appoinment_id = serializers.CharField(source="id")
    patient_name = serializers.CharField(source="patient.full_name")
    doctor_name = serializers.CharField(source="doctor.full_name")
    time_slot_from = serializers.SerializerMethodField("convert_time_slot_from")
    time_slot_to = serializers.SerializerMethodField("convert_time_slot_to")
    class Meta:
        model = AppointmentMaster
        fields = (
            "appoinment_id","patient_name","doctor_name","appointment_type","appointment_code","date","time_slot_from","time_slot_to",
            "is_active","created_dt","updated_dt"
            )
        
    def convert_time_slot_from(self,obj):
        time_slot_from_str = str(obj.time_slot_from)
        time_slot_from_obj = datetime.strptime(time_slot_from_str, "%H:%M:%S").time()
        formatted_time_slot_from = time_slot_from_obj.strftime("%I:%M %p")
        return formatted_time_slot_from
    
    def convert_time_slot_to(self,obj):
        time_slot_to_str = str(obj.time_slot_to)
        time_slot_to_obj = datetime.strptime(time_slot_to_str, "%H:%M:%S").time()
        formatted_time_slot_to = time_slot_to_obj.strftime("%I:%M %p")
        return formatted_time_slot_to
    
    def insert(self,request):
        try:
            patient_obj = request.get("patient_obj",None)
            doctor_obj = request.get("doctor_obj",None)
            appointment_type = request.get("appointment_type",None)
            symptoms = request.get("symptoms",None)
            date = request.get("date",None)
            time_slot_from = request.get("time_slot_from",None)
            time_slot_to = request.get("time_slot_to",None)
            added_by = request.get("user_master_obj",None)

            insert_dict = {}

            if patient_obj:
                insert_dict["patient"] = patient_obj
            if doctor_obj:
                insert_dict["doctor"] = doctor_obj
            if appointment_type:
                insert_dict["appointment_type"] = appointment_type
            if date:
                insert_dict["date"] = date
            if time_slot_from:
                insert_dict["time_slot_from"] = shared.time_converter(time_slot_from)
            if time_slot_to:
                insert_dict["time_slot_to"] = shared.time_converter(time_slot_to)
            if added_by:
                insert_dict["added_by"] = added_by
            
            obj_created = AppointmentMaster.objects.create(**insert_dict)
            return obj_created
            
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
        
    def update_data(self,request,appointment_obj):
        try:
            if request.get("patient_id"):
               appointment_obj.patient_id = request.get("patient_id")
            if request.get("doctor_id"):
               appointment_obj.doctor_id = request.get("doctor_id")
            if request.get("appointment_type"):
               appointment_obj.appointment_type = request.get("appointment_type")
            if request.get("symptoms"):
               appointment_obj.symptoms = request.get("symptoms")
            if request.get("date"):
               appointment_obj.date = request.get("date")
            if request.get("time_slot_from"):
               time_slot_from = shared.time_converter(request.get("time_slot_from"))
               appointment_obj.time_slot_from = time_slot_from
            if request.get("time_slot_to"):
               time_slot_to = shared.time_converter(request.get("time_slot_to"))
               appointment_obj.time_slot_to = time_slot_to
            if request.get("user_master_obj"):
               appointment_obj.updated_by = request.get("user_master_obj")
            appointment_obj.save()
            return True
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)

class AppointmentDetailsSerializer(serializers.ModelSerializer):
    appointment_detail_id = serializers.IntegerField(source="id")
    symptom_name = serializers.CharField(source="symptom.name")
    class Meta:
        model = AppointmentDetails
        fields = ("appointment_detail_id","symptom_name","created_dt","updated_dt","is_active")

    def insert(self,request,appointment_obj):
        try:
            symptop_id_list = request.get("symptom_id_list")
            user_obj = request.get("user_master_obj")
            df = pd.DataFrame({"symptom_id":symptop_id_list})
            df["appointment"] = appointment_obj
            df["added_by"] = user_obj
            df_dct = df.to_dict("records")
            instances = [AppointmentDetails(**item) for item in df_dct]             
            AppointmentDetails.objects.bulk_create(instances)
            return True
        except Exception as ex:
            return False

        
class AddFamilyMemberSerializer(serializers.ModelSerializer):
    family_member_id = serializers.IntegerField(source="id")
    patient_id = serializers.CharField(source="patient.id")
    patient_name = serializers.CharField(source="patient.full_name")
    patient_mobile_number = serializers.CharField(source="patient.mobile_number")
    patient_email_id = serializers.CharField(source="patient.email_id")
    class Meta:
        model = PatientFamilyDetails
        fields = ("family_member_id","mobile_number","first_name","last_name","full_name","address_1","address_2","city","state","pincode",
                  "age","dob","email_id","country","qualification","gender","patient_id","patient_name","patient_mobile_number","patient_email_id")

    def insert(self,request):
        try:
            mobile_number = request.get("mobile_number",None)
            first_name = request.get("first_name",None)
            last_name = request.get("last_name",None)
            address_1 = request.get("address_1",None)
            address_2 = request.get("address_2",None)
            city = request.get("city",None)
            state = request.get("state",None)
            pincode = request.get("pincode",None)
            age = request.get("age",None)
            dob = request.get("dob",None)
            email_id = request.get("email_id",None)
            country = request.get("country",None)
            qualification = request.get("qualification",None)
            full_name = request.get("full_name",None)
            gender = request.get("gender",None)
            patient_obj = request.get("patient_obj",None)
            
            insert_dict = {}
            if mobile_number:
                insert_dict["mobile_number"] = mobile_number 
            if first_name:
                insert_dict["first_name"] = first_name 
            if last_name:
                insert_dict["last_name"] = last_name 
            if address_1:
                insert_dict["address_1"] = address_1 
            if address_2:
                insert_dict["address_2"] = address_2 
            if city:
                insert_dict["city"] = city 
            if state:
                insert_dict["state"] = state 
            if pincode:
                insert_dict["pincode"] = pincode 
            if age:
                insert_dict["age"] = age 
            if dob:
                insert_dict["dob"] = dob 
            if email_id:
                insert_dict["email_id"] = email_id 
            if country:
                insert_dict["country"] = country 
            if qualification:
                insert_dict["qualification"] = qualification 
            if full_name:
                insert_dict["full_name"] = full_name 
            if gender:
                insert_dict["gender"] = gender 
            if patient_obj:
                insert_dict["patient"] = patient_obj 

            family_added = PatientFamilyDetails.objects.create(**insert_dict)
            
            return family_added
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
        
    def update_record(self,request,obj):
        try:
            mobile_number = request.get("mobile_number",None)
            first_name = request.get("first_name",None)
            last_name = request.get("last_name",None)
            address_1 = request.get("address_1",None)
            address_2 = request.get("address_2",None)
            city = request.get("city",None)
            state = request.get("state",None)
            pincode = request.get("pincode",None)
            age = request.get("age",None)
            dob = request.get("dob",None)
            email_id = request.get("email_id",None)
            country = request.get("country",None)
            qualification = request.get("qualification",None)
            full_name = request.get("full_name",None)
            gender = request.get("gender",None)
            
            if mobile_number:
                obj.mobile_number = mobile_number
            if first_name:
                obj.first_name = first_name 
            if last_name:
                obj.last_name = last_name 
            if address_1:
                obj.address_1 = address_1 
            if address_2:
                obj.address_2 = address_2 
            if city:
                obj.city = city 
            if state:
                obj.state = state 
            if pincode:
                obj.pincode = pincode 
            if age:
                obj.age = age 
            if dob:
                obj.dob = dob 
            if email_id:
                obj.email_id = email_id 
            if country:
                obj.country = country 
            if qualification:
               obj.qualification = qualification 
            if full_name:
                obj.full_name = full_name 
            if gender:
                obj.gender = gender 
            obj.save()
            return True
        except Exception as ex:
            return False
