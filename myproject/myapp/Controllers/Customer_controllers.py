# myapp/controllers/customer_controller.py
from ..models import Customer

def create_customer(first_name, last_name, age, monthly_income, phone_number):
    # Calculate the approved limit (36 * monthly_salary) rounded to nearest lakh
    
    
    approved_limit = round(36 * int(monthly_income) / 100000) * 100000
    
    # Create and save the customer to the database
    customer = Customer.objects.create(
        first_name=first_name,
        last_name=last_name,
        age=age,
        monthly_salary=monthly_income,
        approved_limit=approved_limit,
        phone_number=phone_number
    )
    
    return customer
