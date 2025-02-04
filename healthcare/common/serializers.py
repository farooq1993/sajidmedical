from rest_framework import serializers
from healthcare.models.master_model import TransactionMaster, User
from django.contrib.auth.models import User
from django.conf import settings
from healthcare.utils import shared

class MasterModelSerializers(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = "__all__"
        



    # def insert(self,request):
    #     try:
    #         mobile_number = request.get("mobile_number",None)
    #         user_type = request.get("user_type",None)
    #         first_name = request.get("first_name",None)
    #         last_name = request.get("last_name",None)
    #         address_1 = request.get("address_1",None)
    #         address_2 = request.get("address_2",None)
    #         city = request.get("city",None)
    #         state = request.get("state",None)
    #         pincode = request.get("pincode",None)
    #         age = request.get("age",None)
    #         dob = request.get("dob",None)
    #         email_id = request.get("email_id",None)
    #         country = request.get("country",None)
    #         speciality = request.get("speciality",None)
    #         qualification = request.get("qualification",None)
    #         experience = request.get("experience",None)
    #         currently_working_at = request.get("currently_working_at",None)
    #         full_name = request.get("full_name",None)
    #         gender = request.get("gender",None)
            
    #         user_code = shared.user_code(user_type.user_type_name)
    #         insert_dict = {
    #             "user_type":user_type,"user_name":user_code
    #             }
    #         if mobile_number:
    #             insert_dict["mobile_number"] = mobile_number 
    #         if first_name:
    #             insert_dict["first_name"] = first_name 
    #         if last_name:
    #             insert_dict["last_name"] = last_name 
    #         if address_1:
    #             insert_dict["address_1"] = address_1 
    #         if address_2:
    #             insert_dict["address_2"] = address_2 
    #         if city:
    #             insert_dict["city"] = city 
    #         if state:
    #             insert_dict["state"] = state 
    #         if pincode:
    #             insert_dict["pincode"] = pincode 
    #         if age:
    #             insert_dict["age"] = age 
    #         if dob:
    #             insert_dict["dob"] = dob 
    #         if email_id:
    #             insert_dict["email_id"] = email_id 
    #         if country:
    #             insert_dict["country"] = country 
    #         if qualification:
    #             insert_dict["qualification"] = qualification 
    #         if experience:
    #             insert_dict["experience"] = experience 
    #         if currently_working_at:
    #             insert_dict["currently_working_at"] = currently_working_at 
    #         if speciality:
    #             insert_dict["speciality"] = speciality 
    #         if full_name:
    #             insert_dict["full_name"] = full_name 
    #         if gender:
    #             insert_dict["gender"] = gender 

    #         user_created = UserMaster.objects.create(**insert_dict)
    #         is_user_instance = User.objects.create_user(
    #             username = user_code,
    #             password = settings.AUTH_TOKEN_PASSWORD
    #         )
    #         user_created.user = is_user_instance
    #         user_created.save()
    #         return user_created
    #     except Exception as ex:
    #         return False
        
    # def update_record(self,request,obj):
    #     try:
    #         mobile_number = request.get("mobile_number",None)
    #         first_name = request.get("first_name",None)
    #         last_name = request.get("last_name",None)
    #         address_1 = request.get("address_1",None)
    #         address_2 = request.get("address_2",None)
    #         city = request.get("city",None)
    #         state = request.get("state",None)
    #         pincode = request.get("pincode",None)
    #         age = request.get("age",None)
    #         dob = request.get("dob",None)
    #         email_id = request.get("email_id",None)
    #         country = request.get("country",None)
    #         qualification = request.get("qualification",None)
    #         experience = request.get("experience",None)
    #         full_name = request.get("full_name",None)
    #         gender = request.get("gender",None)
    #         doctor = request.get("doctor",None)
            
    #         if mobile_number:
    #             obj.mobile_number = mobile_number
    #         if first_name:
    #             obj.first_name = first_name 
    #         if last_name:
    #             obj.last_name = last_name 
    #         if address_1:
    #             obj.address_1 = address_1 
    #         if address_2:
    #             obj.address_2 = address_2 
    #         if city:
    #             obj.city = city 
    #         if state:
    #             obj.state = state 
    #         if pincode:
    #             obj.pincode = pincode 
    #         if age:
    #             obj.age = age 
    #         if dob:
    #             obj.dob = dob 
    #         if email_id:
    #             obj.email_id = email_id 
    #         if country:
    #             obj.country = country 
    #         if qualification:
    #            obj.qualification = qualification 
    #         if experience:
    #             obj.experience = experience 
    #         if full_name:
    #             obj.full_name = full_name 
    #         if gender:
    #             obj.gender = gender 
    #         if doctor:
    #             obj.doctor = doctor 
    #         obj.save()
    #         return True
    #     except Exception as ex:
    #         return False
        

class TransactionSerializer(serializers.ModelSerializer):
    # payment_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = TransactionMaster
        fields = ('amount','razorpay_order_id','is_paid')