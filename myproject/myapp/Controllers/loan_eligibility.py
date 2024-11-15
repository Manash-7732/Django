from decimal import Decimal
from datetime import datetime
from myapp.models import Customer, LoanData
from django.db.models import Sum, F

def calculate_credit_score(customer_id):
    customer = Customer.objects.get(customer_id=customer_id)
    loans = LoanData.objects.filter(customer_id=customer_id)
    

    # Component 1: Past Loans Paid on Time
    total_emis = loans.aggregate(Sum('tenure'))['tenure__sum'] or 0
    on_time_emis = loans.aggregate(Sum('emis_paid_on_time'))['emis_paid_on_time__sum'] or 0
    timely_payment_ratio = on_time_emis / total_emis if total_emis > 0 else 0
    score_deduction_on_time = 30 if timely_payment_ratio < 0.5 else 0

    # Component 2: Number of Loans Taken in the Past
    num_loans_taken = loans.count()
    score_deduction_num_loans = 10 if num_loans_taken > 5 else 0

    # Component 3: Loan Activity in Current Year
    current_year_loans = loans.filter(start_date__year=datetime.now().year).count()
    score_deduction_current_year = 20 if current_year_loans > 1 else 0

    # Component 4: Loan Approved Volume
    loan_approved_volume = loans.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0
    score_deduction_volume = min(loan_approved_volume / 1_000_000, 20)

    # Component 5: Total Loans vs Approved Limit
    if loan_approved_volume > customer.approved_limit:
        return 0  # Credit score is 0 if loan volume exceeds approved limit

    # Calculate final credit score
    credit_score = 100 - (score_deduction_on_time + score_deduction_num_loans +
                          score_deduction_current_year + score_deduction_volume)
    
    # Ensure non-negative credit score
    credit_score = max(credit_score, 0)
    return credit_score

def check_loan_eligibility(customer_id, loan_amount, interest_rate, tenure):
    customer = Customer.objects.get(customer_id=customer_id)
    loans = LoanData.objects.filter(customer_id=customer_id)
    credit_score = calculate_credit_score(customer_id)
    print(credit_score)

    # Sum up all current EMIs
    total_current_emi = loans.aggregate(Sum('monthly_repayment'))['monthly_repayment__sum'] or Decimal("0")
    print("Manash Raj")

    print(total_current_emi);
    print(Decimal("0.5") * customer.monthly_salary);

    # Check EMI constraint (EMIs must not exceed 50% of monthly salary)
    if total_current_emi > Decimal("0.5") * customer.monthly_salary:
        return {
            "customer_id": customer_id,
            "approval": False,
            "interest_rate": interest_rate,
            "corrected_interest_rate": interest_rate,
            "tenure": tenure,
            "monthly_installment": 0,
            "message": "EMI exceeds 50% of monthly salary"
        }

    
    if total_current_emi + loan_amount > customer.approved_limit:
        return {
            "customer_id": customer_id,
            "approval": False,
            "interest_rate": interest_rate,
            "corrected_interest_rate": interest_rate,
            "tenure": tenure,
            "monthly_installment": 0,
            "message": "Current loan amount exceeds approved limit"
        }

    # Determine loan approval and interest rate based on credit score
    approval = False
    corrected_interest_rate = interest_rate
    if credit_score > 50:
        approval = True
    elif 50 >= credit_score > 30:
        approval = True
        corrected_interest_rate = max(interest_rate, Decimal("12"))
    elif 30 >= credit_score > 10:
        approval = True
        corrected_interest_rate = max(interest_rate, Decimal("16"))

    # Calculate the monthly installment (EMI) if loan is approved
    if approval:
        monthly_installment = (loan_amount * corrected_interest_rate / 100) / 12
    else:
        monthly_installment = 0

    return {
        "customer_id": customer_id,
        "approval": approval,
        "interest_rate": float(interest_rate),
        "corrected_interest_rate": float(corrected_interest_rate),
        "tenure": tenure,
        "monthly_installment": float(monthly_installment),
        "message": "Loan approval status and interest rate based on credit score"
    }
