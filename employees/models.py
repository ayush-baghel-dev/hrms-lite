from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class Employee(models.Model):
    employee_id = models.CharField(max_length=50, unique=True, db_index=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"

    def clean(self):
        if self.email:
            self.email = self.email.lower()


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['employee', 'date']
        indexes = [
            models.Index(fields=['employee', 'date']),
        ]

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"

    def clean(self):
        if self.status not in ['Present', 'Absent']:
            raise ValidationError({'status': 'Status must be either Present or Absent'})