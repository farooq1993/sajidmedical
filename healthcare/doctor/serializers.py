from rest_framework import serializers
from healthcare.models.master_model import UserMaster
from django.conf import settings
from django.contrib.auth.models import User
from healthcare.utils import shared,error_messages,constants,logging_utils
from rest_framework.response import Response
from rest_framework import status
from healthcare.models.doctor_model import MedicineMaster,Prescription,TestMaster,PrescriptionMedicineDetails,PrescriptionTestDetails
import pandas as pd
class DoctorSerializer(serializers.ModelSerializer):
    doctor_id = serializers.IntegerField(source='id')
    user_type = serializers.CharField(source='user_type.user_type_name')
    class Meta:
        model = UserMaster
        fields = (
            'doctor_id','first_name','last_name','full_name','email_id','user_type','mobile_number','address_1','address_2','state',
            'city','pincode','gender','experience','speciality','currently_working_at','is_verified'
        )
    
    def update_record(self,request,obj):
        try:
            mobile_number = request.get("mobile_number",None)
            full_name = request.get("full_name",None)
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
            gender = request.get("gender",None)
            currently_working_at = request.get("currently_working_at",None)
            speciality = request.get("speciality",None)
            experience = request.get("experience",None)
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
            if currently_working_at:
                obj.currently_working_at = currently_working_at 
            if speciality:
                obj.speciality = speciality 
            if experience:
                obj.experience = experience 
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
class DoctorStaffManagementSerializer(serializers.ModelSerializer):
    staff_id = serializers.IntegerField(source='id')
    class Meta:
        model = UserMaster
        fields = (
            'staff_id','first_name','last_name','full_name','mobile_number','state','address_1','address_2','city',
            'pincode','gender','experience',
        )

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
            experience = request.get("experience",None)
            full_name = request.get("full_name",None)
            gender = request.get("gender",None)
            doctor_obj = request.get("doctor_obj",None)
            user_type_obj = request.get("user_type_obj",None)
            
            user_code = shared.user_code(constants.DOCTOR_STAFF)
            insert_dict = {
                "user_name":user_code
                }
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
            if experience:
                insert_dict["experience"] = experience 
            if full_name:
                insert_dict["full_name"] = full_name 
            if gender:
                insert_dict["gender"] = gender 
            if doctor_obj:
                insert_dict["doctor"] = doctor_obj
            if user_type_obj:
                insert_dict["user_type"] = user_type_obj 

            user_created = UserMaster.objects.create(**insert_dict)
            is_user_instance = User.objects.create_user(
                username = user_code,
                password = settings.AUTH_TOKEN_PASSWORD
            )
            user_created.user = is_user_instance
            user_created.save()
            return user_created
        except Exception as ex:
            return Response(data=error_messages.STAFF_ACCOUNT_CREATED,status=status.HTTP_412_PRECONDITION_FAILED)

    def update_staff_record(self,request,obj):
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
            experience = request.get("experience",None)
            full_name = request.get("full_name",None)
            gender = request.get("gender",None)
            doctor = request.get("doctor",None)
            
            if mobile_number:
                obj.mobile_number = mobile_number
            if email_id:
                obj.email_id = email_id
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
            if country:
                obj.country = country 
            if qualification:
               obj.qualification = qualification 
            if experience:
                obj.experience = experience 
            if full_name:
                obj.full_name = full_name 
            if gender:
                obj.gender = gender 
            if doctor:
                obj.doctor = doctor 
            obj.save()
            return True
        except Exception as ex:
                return Response(data=error_messages.STAFF_ACCOUNT_CREATED,status=status.HTTP_412_PRECONDITION_FAILED)
        
class MedicineSerializer(serializers.ModelSerializer):
    added_by = serializers.CharField(source = "added_by.user_type.user_type_name")
    updated_by = serializers.CharField(source = "added_by.user_type.user_type_name")
    medicine_id = serializers.IntegerField(source = "id")
    class Meta:
        model = MedicineMaster
        fields = (
            "medicine_id","drug","strength","medicine_name","medicine_type","cost_of_medicine","purpose","added_by","updated_by","manufacturer",
            "acronym","added_by","created_dt","updated_dt"
            )

    def insert(self,request):
        try:
            medicine_name = request.get("medicine_name",None)
            medicine_type = request.get("medicine_type",None)
            cost_of_medicine =request.get("cost_of_medicine",None)
            purpose =request.get("purpose",None)
            manufacturer =request.get("manufacturer",None)
            acronym =request.get("acronym",None)
            strength =request.get("strength",None)
            drug =request.get("drug",None)
            added_by =request.get("added_by",None)

            insert_dict = {}

            if strength:
                insert_dict["strength"] = strength
            if drug:
                insert_dict["drug"] = drug
            if medicine_name:
                insert_dict["medicine_name"] = medicine_name
            if medicine_type:
                insert_dict["medicine_type"] = medicine_type
            if cost_of_medicine:
                insert_dict["cost_of_medicine"] = cost_of_medicine
            if purpose:
                insert_dict["purpose"] = purpose
            if manufacturer:
                insert_dict["manufacturer"] = manufacturer
            if acronym:
                insert_dict["acronym"] = acronym
            if added_by:
                insert_dict["added_by"] = added_by

            is_medicine_credted = MedicineMaster.objects.create(**insert_dict)
            return is_medicine_credted
        except Exception as ex:
            logging_utils.helper_error("doctor_serializer","MedicineSerializer-->insert",ex)
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_412_PRECONDITION_FAILED)
    

    def updated_medicine(self,request,obj):
        try:
            medicine_name = request.get("medicine_name",None)
            medicine_type = request.get("medicine_type",None)
            cost_of_medicine =request.get("cost_of_medicine",None)
            purpose =request.get("purpose",None)
            manufacturer =request.get("manufacturer",None)
            acronym =request.get("acronym",None)
            user_master_obj =request.get("user_master_obj",None)
            is_verified =request.get("is_verified",None)


            if medicine_name:
                obj.manage_medicine = medicine_name
            if medicine_type:
                obj.medicine_type = medicine_type
            if cost_of_medicine:
                obj.cost_of_medicine = cost_of_medicine
            if purpose:
                obj.purpose = purpose
            if manufacturer:
                obj.manufacturer = manufacturer
            if acronym:
                obj.acronym = acronym
            if user_master_obj:
                obj.updated_by = user_master_obj
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

class IntegerArrayField(serializers.ListField):
    child = serializers.IntegerField()
class PrescriptionSerializer(serializers.ModelSerializer):
    prescription_id = serializers.IntegerField(source="id")
    test_list = IntegerArrayField()
    medicine_list = IntegerArrayField()
    class Meta:
        model = Prescription
        fields = (
            "prescription_id","doctor","patient","next_consult","added_by","regime","tenure","medicine_instruction",
            "advoice_list","test_list","medicine_list"
            )

    def insert(self,request):
        try:
            doctor = request.get("doctor_obj",None)
            patient = request.get("patient_obj",None)
            medicine_recomended_from_inside = request.get("medicine_recomended_from_inside",None)
            medicine_recomended_from_outside = request.get("medicine_recomended_from_outside",None)
            test_advice = request.get("test_advice",None)
            other_advice = request.get("other_advice",None)
            next_consult = request.get("next_consult",None)
            added_by = request.get("added_by",None)
            regime = request.get("regime",None)
            tenure = request.get("tenure",None)
            medicine_instruction = request.get("medicine_instruction",None)
            import json
            advoice_list = json.loads(request.get("advoice_list",None))
            test_list = request.get("test_list",None)
            medicine_list = request.get("medicine_list",None)

            insert_dict = {}

            if advoice_list:
                insert_dict["advoice_list"] = advoice_list
            if test_list:
                insert_dict["test_list"] = test_list
            if medicine_list:
                insert_dict["medicine_list"] = medicine_list
            if regime:
                insert_dict["regime"] = regime
            if tenure:
                insert_dict["regime"] = regime
            if medicine_instruction:
                insert_dict["medicine_instruction"] = medicine_instruction
            if doctor:
                insert_dict["doctor"] = doctor
            if patient:
                insert_dict["patient"] = patient
            if medicine_recomended_from_inside:
                insert_dict["medicine_recomended_from_inside"] = medicine_recomended_from_inside
            if medicine_recomended_from_outside:
                insert_dict["medicine_recomended_from_outside"] = medicine_recomended_from_outside
            if test_advice:
                insert_dict["test_advice"] = test_advice
            if other_advice:
                insert_dict["other_advice"] = other_advice
            if next_consult:
                insert_dict["next_consult"] = next_consult
            if added_by:
                insert_dict["added_by"] = added_by

            is_created = Prescription.objects.create(**insert_dict)
            return is_created
        except Exception as ex:
            return False
        
    def update_prescription(self,request,obj):
        try:
            doctor = request.get("doctor",None)
            patient = request.get("patient",None)
            medicine_recomended_from_inside = request.get("medicine_recomended_from_inside",None)
            medicine_recomended_from_outside = request.get("medicine_recomended_from_outside",None)
            advice = request.get("advice",None)
            test_advice = request.get("test_advice",None)
            other_advice = request.get("other_advice",None)
            next_consult = request.get("next_consult",None)

            if doctor:
                obj.doctor = doctor
            if patient:
                obj.patient = patient
            if medicine_recomended_from_inside:
                obj.medicine_recomended_from_inside = medicine_recomended_from_inside
            if medicine_recomended_from_outside:
                obj.medicine_recomended_from_outside = medicine_recomended_from_outside
            if advice:
                obj.advice = advice
            if test_advice:
                obj.test_advice = test_advice
            if other_advice:
                obj.other_advice = other_advice
            if next_consult:
                obj.next_consult = next_consult
            obj.save()
            return True
        except Exception as ex:
            return False

class PrescriptionMedicineDetailserializer(serializers.ModelSerializer):

    def insert(self,request,obj):
        try:
            import json
            medicine_lst = json.loads(request.get("medicine_lst", None))
            added_by = request.get("added_by", None)
            test_lst = request.get("test_lst", None)
            df = ["medicine_id","tenure","regime","instruction","test_id"]
            df = pd.DataFrame(columns = df)
            if medicine_lst:
                df = pd.DataFrame(medicine_lst)
                df["prescription_id"] = obj.id
                df["added_by"] = added_by
                insert_dict = df.to_dict("records")
                instances = [PrescriptionMedicineDetails(**item) for item in insert_dict]
                PrescriptionMedicineDetails.objects.bulk_create(instances)
                return True
            else:
                return False
        except Exception as ex:
            return False
        
class PrescriptionTestDetailsSerializer(serializers.Serializer):

    def insert(self,request,obj):
        try:
            import json
            test_lst = request.get("test_lst", None)
            added_by = request.get("added_by", None)
            if test_lst:
                test_lst = json.loads(test_lst)
                df = pd.DataFrame(test_lst)
                df["prescription_id"] = obj.id
                df["added_by"] = added_by
                insert_dict = df.to_dict("records")
                instances = [PrescriptionTestDetails(**item) for item in insert_dict]
                PrescriptionTestDetails.objects.bulk_create(instances)
                return True
            else:
                return False
        except Exception as ex:
            return False

class TestMasterSerializer(serializers.ModelSerializer):
    test_id = serializers.IntegerField(source="id")
    added_by = serializers.CharField(source = "added_by.user_type.user_type_name")
    updated_by = serializers.CharField(source = "updated_by.user_type.user_type_name")

    class Meta:
        model = TestMaster
        fields = ("test_id","name","body_part","added_by","updated_by","is_active")
            
    
    def insert(self,request):
        try:
            user_obj = request.get("user_master_obj",None)
            name = request.get("name",None)
            body_part = request.get("body_part",None)

            insert_dict = {}   
            if name:
                insert_dict["name"] = name
            if body_part:
                insert_dict["body_part"] = body_part
            insert_dict["added_by"] = user_obj
            TestMaster.objects.create(**insert_dict)
            return True
        except Exception as ex:
            logging_utils.helper_error("doctor_serializer","TestMasterSerializer-->insert",ex)
            return False

