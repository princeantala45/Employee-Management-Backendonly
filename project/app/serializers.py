from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from datetime import timedelta,datetime
from decimal import Decimal

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data) -> User:
        
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user
    
    
class EmployeeRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRole
        fields = '__all__'
        read_only_fields = ['user']

class EmployeeLeaveSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeave
        fields = '__all__'
        read_only_fields = ['user']
    

class EmployeeSalarySerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSalary
        fields = '__all__'
    
    def validate(self, data):
        if data['salary'] < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return data


class EmployeeAttandenceSerializers(serializers.ModelSerializer):

    class Meta:
        model = EmployeeAttandence
        fields = '__all__'
        read_only_fields = ['work_duration', 'overtime_hours', 'overtime_amount']

    def create(self, validated_data):
        checkin = validated_data['checkin']
        checkout = validated_data['checkout']

        # Calculate work duration
        work_duration = datetime.combine(datetime.today(), checkout) - \
                        datetime.combine(datetime.today(), checkin)

        # Overtime after 9 hours
        nine_hours = timedelta(hours=9)

        if work_duration > nine_hours:
            overtime = work_duration - nine_hours
            overtime_hours = overtime.total_seconds() / 3600
            overtime_amount = Decimal(overtime_hours) * Decimal(300)
        else:
            overtime_hours = 0
            overtime_amount = 0

        validated_data['work_duration'] = work_duration
        validated_data['overtime_hours'] = overtime_hours
        validated_data['overtime_amount'] = overtime_amount

        return super().create(validated_data)