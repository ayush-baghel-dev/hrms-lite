from rest_framework import serializers
from .models import Employee, Attendance
import re

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name', 'email', 'department', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_employee_id(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Employee ID is required")
        return value.strip()

    def validate_full_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Full name is required")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Full name must be at least 2 characters")
        return value.strip()

    def validate_email(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Email is required")
        
        email = value.strip().lower()
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_regex, email):
            raise serializers.ValidationError("Enter a valid email address")
        
        if self.instance:
            if Employee.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise serializers.ValidationError("An employee with this email already exists")
        else:
            if Employee.objects.filter(email=email).exists():
                raise serializers.ValidationError("An employee with this email already exists")
        
        return email

    def validate_department(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Department is required")
        return value.strip()


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id_display = serializers.CharField(source='employee.employee_id', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'employee_name', 'employee_id_display']

    def validate_status(self, value):
        if value not in ['Present', 'Absent']:
            raise serializers.ValidationError("Status must be either 'Present' or 'Absent'")
        return value

    # def validate(self, data):
    #     employee = data.get('employee')
    #     date = data.get('date')

    #     if self.instance:
    #         if Attendance.objects.exclude(pk=self.instance.pk)\
    #                 .filter(employee=employee, date=date).exists():
    #             raise serializers.ValidationError(
    #                 "Attendance already exists for this employee on this date."
    #             )
    #     else:
    #         if Attendance.objects.filter(employee=employee, date=date).exists():
    #             raise serializers.ValidationError(
    #                 "Attendance already exists for this employee on this date."
    #             )

    #     return data