from healthcare.medical_admin import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^appointment_history/$',views.AppointmentHistory.as_view(),name='appointment_history'),
    re_path(r'^get_doctor/$',views.GetDoctor.as_view(),name='get_doctor'),
    re_path(r'^manage_doctor/$',views.ManageDoctor.as_view(),name='manage_doctor'),
    re_path(r'^get_patient/$',views.GetPatient.as_view(),name='get_patient'),
    re_path(r'^manage_patient/$',views.ManagePatient.as_view(),name='manage_patient'),
    re_path(r'^get_medicine/$',views.GetMedicine.as_view(),name='get_medicine'),
    re_path(r'^manage_medicine/$',views.ManageMedicine.as_view(),name='manage_medicine'),
    # re_path(r'^add_blog/$',views.AddBlog.as_view(),name='add_blog'),
    # re_path(r'^get_blog/$',views.GetBlog.as_view(),name='get_blog'),
    # re_path(r'^manage_blog/$',views.ManageBlog.as_view(),name='manage_blog'),
    re_path(r'^add_symptoms/$',views.AddSymptoms.as_view(),name='add_symptoms'),
    re_path(r'^get_symptoms/$',views.GetSymptoms.as_view(),name='get_symptoms'),
    re_path(r'^manage_symptoms/$',views.ManageSymptoms.as_view(),name='manage_symptoms'),
]