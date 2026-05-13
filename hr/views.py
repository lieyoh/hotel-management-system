from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Employee, Department
# Create your views here.


class EmployeeList(ListView):
    model = Employee
    template_name = 'hr/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):

        queryset = Employee.objects.all()

        query = self.request.GET.get('q')
        department = self.request.GET.get('department')
        active = self.request.GET.get('is_active')

        if query:
            queryset = queryset.filter(
                Q(employee_id__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__username__icontains=query)
            )
        if department:
            queryset = queryset.filter(department__name=department)
        if active:
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']  # kinukuha nya yung paginated by

        context.update({
            # para mas madali tawagin ginawang dictonary
            'current_page': page_obj.number,
            'last_page': page_obj.paginator.num_pages,
            'prev_num': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next_num': page_obj.next_page_number() if page_obj.has_next() else None,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        })
        return context
