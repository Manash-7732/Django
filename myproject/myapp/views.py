from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, LoanData
from .serializers import CustomerSerializer, LoanDataSerializer
from .Controllers.Customer_controllers import create_customer
from .Controllers.loan_eligibility import check_loan_eligibility
from decimal import Decimal

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        # Extract data from request
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        age = request.data.get('age')
        monthly_income = request.data.get('monthly_income')
        phone_number = request.data.get('phone_number')

        # Check if required fields are provided
        if not first_name or not last_name or not age or not monthly_income or not phone_number:
            return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Call the controller function to create the customer
        customer = create_customer(first_name, last_name, age, monthly_income, phone_number)

        # Serialize and return the newly created customer data
        serializer = self.get_serializer(customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoanDataViewSet(viewsets.ModelViewSet):
    queryset = LoanData.objects.all()
    serializer_class = LoanDataSerializer


@api_view(['POST'])
def check_eligibility(request):
    customer_id = request.data.get('customer_id')
    loan_amount = request.data.get('loan_amount')
    interest_rate = request.data.get('interest_rate')
    tenure = request.data.get('tenure')
    
    if not all([customer_id, loan_amount, interest_rate, tenure]):
        return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    print(customer_id);

    # Call the controller to check eligibility
    result = check_loan_eligibility(customer_id, loan_amount, interest_rate, tenure);
    
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
def process_new_loan(request):
    from decimal import Decimal
    from datetime import date

    # Extract data from request
    customer_id = request.data.get("customer_id")
    loan_amount = Decimal(request.data.get("loan_amount"))
    interest_rate = Decimal(request.data.get("interest_rate"))
    tenure = int(request.data.get("tenure"))

    # Check eligibility using the function
    eligibility_result = check_loan_eligibility(customer_id, loan_amount, interest_rate, tenure)
    loan = LoanData.objects.order_by('-loan_id').first()
    print(eligibility_result["approval"]);
    print(loan.loan_id)

    # If the loan is approved, save it and return relevant response data
    if eligibility_result["approval"]:
        # Creating a new loan entry with emis_paid_on_time initialized to 0
        new_loan = LoanData.objects.create(
            loan_id=str(int(loan.loan_id) + 1),
            customer_id=customer_id,
            loan_amount=loan_amount,
            interest_rate=eligibility_result["corrected_interest_rate"],
            tenure=tenure,
            monthly_repayment=eligibility_result["monthly_installment"],
            emis_paid_on_time=0,  # Initializing EMIs paid on time to 0
            start_date=date.today(),  # Assuming the loan starts today
            end_date=date.today().replace(year=date.today().year + tenure // 12)  # Example end date based on tenure
        )
        new_loan.save()

        return Response({
            "loan_id": new_loan.loan_id,
            "customer_id": customer_id,
            "loan_approved": True,
            "message": "Loan approved and processed successfully.",
            "monthly_installment": float(eligibility_result["monthly_installment"])
        }, status=status.HTTP_201_CREATED)

    # If not approved, return a response with loan_approved as False and an appropriate message
    else:
        return Response({
            "loan_id": None,
            "customer_id": customer_id,
            "loan_approved": False,
            "message": eligibility_result["message"],
            "monthly_installment": 0
        }, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def view_loan_details(request, loan_id):
    try:
        # Retrieve loan by loan_id
        loan = LoanData.objects.get(loan_id=loan_id)
        # Fetch related customer details
        customer = Customer.objects.get(customer_id=loan.customer_id)

        # Construct the response
        response_data = {
            "loan_id": loan.id,
            "customer": {
                "id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone_number": customer.phone_number,
                "age": customer.age
            },
            "loan_amount": float(loan.loan_amount),
            "interest_rate": float(loan.interest_rate),
            "monthly_installment": float(loan.monthly_repayment),
            "tenure": loan.tenure
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except LoanData.DoesNotExist:
        return Response({"message": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)
    except Customer.DoesNotExist:
        return Response({"message": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_loan_details_by_customer_id(request, customer_id):
    try:
        # Retrieve loan by loan_id
        loans = LoanData.objects.all().filter(customer_id=customer_id)
        # Construct the response
        answer = []
        for loan in loans:
            response_data = {
                "loan_id": loan.id,
                "loan_amount": float(loan.loan_amount),
                "interest_rate": float(loan.interest_rate),
                "monthly_installment": float(loan.monthly_repayment),
                "repayments_left": loan.tenure - loan.emis_paid_on_time
            }
            answer.append(response_data)
        
        return Response(answer, status=status.HTTP_200_OK)
    except LoanData.DoesNotExist:
        return Response({"message": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)
    except Customer.DoesNotExist:
        return Response({"message": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)