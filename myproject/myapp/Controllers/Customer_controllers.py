
from ..models import Customer

def create_customer(first_name, last_name, age, monthly_income, phone_number):
   
    
    
    approved_limit = round(36 * int(monthly_income) / 100000) * 100000
    
   
    customer = Customer.objects.create(
        first_name=first_name,
        last_name=last_name,
        age=age,
        monthly_salary=monthly_income,
        approved_limit=approved_limit,
        phone_number=phone_number
    )
    
    return customer
