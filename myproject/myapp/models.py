from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True,null=False)  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(default=30)
    phone_number = models.CharField(max_length=15)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.customer_id}"
      
class LoanData(models.Model):
    customer= models.ForeignKey(Customer, related_name='loan_data', on_delete=models.CASCADE)  
    loan_id = models.CharField(max_length=20, unique=True, editable=True)  
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    tenure = models.IntegerField()  
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)  
    emis_paid_on_time = models.IntegerField(default=0) 
    start_date = models.DateField()  
    end_date = models.DateField()  

    def __str__(self):
        return f"Loan {self.loan_id} - Customer {self.customer.customer_id}"