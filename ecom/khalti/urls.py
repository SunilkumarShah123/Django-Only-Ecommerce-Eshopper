from django.urls import path

from .views import *

urlpatterns = [
path('initiate-khalti-payment/<int:id>/', initiate_khalti_payment, name='initiate_khalti_payment'),
path('verify-khalti/', verifyKhalti, name='verify_khalti'),
]