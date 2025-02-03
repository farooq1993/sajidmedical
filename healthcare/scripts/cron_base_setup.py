import os
import sys
import django
import logging

# proj_path = "C://Users//OtherWork//Desktop//Helath_services//HealthcareProductModule//medical_services//"
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commons.settings")
proj_path = "/root/medical_services/HealthcareProductModule/medical_services/"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commons.settings")
sys.path.append(proj_path)
django.setup()
logger = logging.getLogger('healthcare')
logger_excp = logging.getLogger('healthcare_excp')
