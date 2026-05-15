from django.contrib import admin
from . models import Employee, Attendance, Shift, Department, LeaveRequest, Payroll
# Register your models here.
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Shift)
admin.site.register(Department)
admin.site.register(LeaveRequest)
admin.site.register(Payroll)
