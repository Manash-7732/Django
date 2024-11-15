from rest_framework import serializers
from .models import LoanData, Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class LoanDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanData
        fields = '__all__'
