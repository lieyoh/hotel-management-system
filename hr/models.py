from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    floor = models.IntegerField(null=True, blank=True)


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=100)
    employee_age = models.PositiveIntegerField()
    contact_no = models.CharField(max_length=15, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"


class Shift(models.Model):
    SHIFT_NAMES = [('MORNING', 'Morning'),
                   ('EVENING', 'Evening'),
                   ('NIGHT', 'Night')]
    name = models.CharField(max_length=10, choices=SHIFT_NAMES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name} ({self.start_time}-{self.end_time})"


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('employee', 'date')


class LeaveRequest(models.Model):
    STATUS_CHOICES = [('PENDING', 'Pending'), ('APPROVED',
                                               'Approved'), ('REJECTED', 'Rejected')]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='PENDING')


class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
