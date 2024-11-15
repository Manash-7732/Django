from myapp.models import Customer

def create_customer(f_name, last_name, age, monthly_income, phone_number):
    try:
        approved_limit = round(36 * int(monthly_income) / 100000) * 100000
        customer = Customer.objects.create(
            first_name=f_name,
            last_name=last_name,
            age=age,
            monthly_salary=monthly_income,
            approved_limit=approved_limit,
            phone_number=phone_number
        )
        return customer
    except Exception as e:
        print(f"error -> {e}")
