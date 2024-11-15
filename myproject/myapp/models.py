from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True,null=False)  # Automatically increments
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(default=30)
    phone_number = models.CharField(max_length=15)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.customer_id}"
      
class LoanData(models.Model):
    customer= models.ForeignKey(Customer, related_name='loan_data', on_delete=models.CASCADE)  # Link to Customer
    loan_id = models.CharField(max_length=20, unique=True, editable=True)  # Unique loan identifier
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of the loan
    tenure = models.IntegerField()  # Loan tenure in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Interest rate of the loan
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)  # Monthly repayment amount (EMI)
    emis_paid_on_time = models.IntegerField(default=0)  # Number of EMIs paid on time
    start_date = models.DateField()  # Start date of the loan
    end_date = models.DateField()  # End date of the loan

    def __str__(self):
        return f"Loan {self.loan_id} - Customer {self.customer.customer_id}"