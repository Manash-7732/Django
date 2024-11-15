from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, LoanDataViewSet,check_eligibility,process_new_loan,view_loan_details, view_loan_details_by_customer_id

router = DefaultRouter()
router.register(r'register', CustomerViewSet)
router.register(r'loans', LoanDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('check-eligibility/', check_eligibility, name='check_eligibility'),
    path('process-loan/', process_new_loan, name='process_new_loan'),
    path('view-loan/<int:loan_id>/', view_loan_details, name='view_loan_details'),
    path('view-loans/<int:customer_id>/', view_loan_details_by_customer_id, name='view_loan_details_by_customer_id'),
]
