from rest_framework import serializers
from healthcare.models.master_model import UserMaster
from healthcare.models.master_model import SymptomMaster,SymptomDetails
from rest_framework.response import Response
from healthcare.utils import error_messages,shared,constants
import pandas as pd
from rest_framework import status

class SymptomMasterSerializer(serializers.ModelSerializer):
    body_part_id = serializers.IntegerField(source="id")
    class Meta:
        model = SymptomMaster
        fields = ("body_part_id","body_part_name","added_by","updated_by","is_active","created_dt","updated_dt")

    def insert(self,request):
        try:
            body_part_name = request.get('body_part_name', None)
            user_obj = request.get('user_master_obj', None)
            insert_dict = {}

            if body_part_name:
              insert_dict['body_part_name'] = body_part_name
            
            if user_obj:
              insert_dict['added_by'] = user_obj
                         
            is_created = SymptomMaster.objects.create(**insert_dict)
            return is_created
        except Exception as ex:
            pass
    
    def update_symptom(self,request,obj):
        try:
            body_part_name = request.get('body_part_name', None)
            user_obj = request.get("user_obj",None)
            if body_part_name:
                obj.body_part_name = body_part_name
            if user_obj:
                obj.added_by = user_obj
            obj.save()
            return obj
        except Exception as ex:
            return Response(data=error_messages.SOMETHING_WENT_WRONG,status=status.HTTP_400_BAD_REQUEST)
class SymptomDetailSerializer(serializers.ModelSerializer):
    symptom_id = serializers.IntegerField(source="id")
    symptom_name = serializers.CharField(source="name")
    class Meta:
        model = SymptomDetails
        fields = ("symptom_id","symptom_name","added_by","updated_by","is_active","created_dt","updated_dt")

    def insert(self,request,system_master_obj):
        try:
            symptom_detail_name_list = request.get('symptom_detail_name_list', None)
            user_obj = request.get('user_master_obj', None)
            
            df = pd.DataFrame({"name":symptom_detail_name_list})
            df["symptoms"] = system_master_obj
            df["added_by"] = user_obj
            df = df.to_dict('records')
            instances = [SymptomDetails(**item) for item in df]             
            SymptomDetails.objects.bulk_create(instances)
            return True
        except Exception as ex:
            return False