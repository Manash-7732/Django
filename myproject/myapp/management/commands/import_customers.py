import csv
from django.core.management.base import BaseCommand
from myapp.models import LoanData, Customer
from django.db import IntegrityError
from datetime import datetime

class Command(BaseCommand):
    help = 'Import data from CSV into the LoanData table'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                   
                    start_date = None
                    end_date = None
                    
                   
                    if row['start_date']:
                        try:
                            start_date = datetime.strptime(row['start_date'], '%m/%d/%Y').date() 
                        except ValueError:
                            self.stdout.write(self.style.WARNING(f"Invalid start_date format for Loan ID {row['loan_id']}"))
                    
                    if row['end_date']:
                        try:
                            end_date = datetime.strptime(row['end_date'], '%m/%d/%Y').date() 
                        except ValueError:
                            self.stdout.write(self.style.WARNING(f"Invalid end_date format for Loan ID {row['loan_id']}"))

                
                    try:
                        customer_instance = Customer.objects.get(customer_id=row['customer_id'])
                    except Customer.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Customer with ID {row['customer_id']} not found for Loan ID {row['loan_id']}"))
                        continue  

                  
                    LoanData.objects.create(
                        Customer=customer_instance, 
                        loan_id=row['loan_id'],  
                        loan_amount=row['loan_amount'],
                        tenure=row['tenure'],
                        interest_rate=row['interest_rate'],
                        monthly_repayment=row['monthly_repayment'],
                        emis_paid_on_time=row['emis_paid_on_time'],
                        start_date=start_date, 
                        end_date=end_date  
                    )
                    self.stdout.write(self.style.SUCCESS(f"Added Loan ID {row['loan_id']}"))

                except IntegrityError:
                    self.stdout.write(self.style.WARNING(f"Skipped Loan ID {row['loan_id']} due to duplicate loan ID"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error importing Loan ID {row['loan_id']}: {str(e)}"))
