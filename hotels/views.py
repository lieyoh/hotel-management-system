from django.shortcuts import render
from users.decorators import role_required

@role_required(allowed_roles=['ADMIN', 'MANAGER'])
def admin_dashboard(request):
    return render(request, 'hotel/admin_panel.html')

@role_required(allowed_roles=['STAFF'])
def staff_dashboard(request):
    return render(request, 'hotel/staff_panel.html')

