from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.contrib.auth import get_user_model
from .forms import AdminUserCreationForm
from django.core.exceptions import PermissionDenied
from axes.models import AccessAttempt
from axes.utils import reset
from axes.handlers.proxy import AxesProxyHandler
from django.contrib.auth.views import LoginView
from django.utils import timezone


from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
from axes.handlers.proxy import AxesProxyHandler

admin_required = user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')

User = get_user_model()

class CustomLoginView(LoginView):
    ATTEMPT_LIMIT = 3

    def form_invalid(self, form):
        attempts = self.request.session.get('login_attempts', 0) + 1
        self.request.session['login_attempts'] = attempts
        self.request.session.modified = True

        remaining = self.ATTEMPT_LIMIT - attempts

        if remaining > 0:
            messages.error(
                self.request,
                f"Login Failed: You have {remaining} attempt(s) remaining."
            )
        else:
            messages.error(
                self.request,
                "Account Locked: Too many failed attempts. Please contact the Admin."
            )

        # Redirect back to GET instead of re-rendering the form.
        # This clears the inputs AND prevents refresh from re-submitting the POST.
        return redirect(self.request.path)

    def form_valid(self, form):
        self.request.session.pop('login_attempts', None)
        return super().form_valid(form)

@login_required
def login_success_redirect(request):
    user = request.user
    if user.role == user.Role.ADMIN:
        return redirect("users:admin_dashboard")
    elif user.role == user.Role.MANAGER:
        return redirect("users:manager_dashboard")
    elif user.role == user.Role.STAFF:
        return redirect("users:staff_dashboard")
    else:
        return redirect("customer_dashboard")
    
#ADMIN
@login_required
def admin_view(request):
    if request.user.role != 'ADMIN':
        raise PermissionDenied
    return render(request, 'custom_admin/dashboard.html')


#MANAGER
@login_required
def manager_view(request):
    if request.user.role != 'MANAGER':
        raise PermissionDenied
    return render(request, 'manager/dashboard.html')

#STAFF
@login_required
def staff_view(request):
    if request.user.role != 'STAFF':
        raise PermissionDenied
    return render(request, 'staff/dashboard.html')


# TAGA CREATE NG USER VIEW
@login_required
def create_user_view(request):
    if request.user.role != 'ADMIN':
        raise PermissionDenied

    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('users:admin_dashboard')
        else:
            # ITO ANG MAGPAPAKITA NG MALI SA TERMINAL
            print("--- FORM ERRORS ---")
            print(form.errors)
            print("-------------------")
    else:
        form = AdminUserCreationForm()
    
    return render(request, 'custom_admin/create_user.html', {'form': form})


@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class ToggleUserBlockView(View):

    def post(self, request, user_id):
        target_user = get_object_or_404(User, pk=user_id)

        if target_user == request.user:
            return self._respond(request, False, "You cannot block your own account.", target_user)

        if target_user.is_superuser and not request.user.is_superuser:
            return self._respond(request, False, "You do not have permission to block a superuser.", target_user)

        if target_user.is_active:
            # --- BLOCK ---
            target_user.is_active = False
            target_user.save(update_fields=["is_active"])

            attempt, created = AccessAttempt.objects.get_or_create(
                username=target_user.get_username(),
                defaults={
                    "ip_address": "0.0.0.0",
                    "user_agent": "admin-block",
                    "attempt_time": timezone.now(),
                    "failures_since_start": 999,
                },
            )
            if not created:
                AccessAttempt.objects.filter(
                    username=target_user.get_username()
                ).update(failures_since_start=999)

            action = "blocked"
            message = f"User '{target_user.get_username()}' has been blocked successfully."
        else:
            # --- UNBLOCK ---
            target_user.is_active = True
            target_user.save(update_fields=["is_active"])

            reset(username=target_user.get_username())

            action = "unblocked"
            message = f"User '{target_user.get_username()}' has been unblocked successfully."

        return self._respond(request, True, message, target_user, action)

    def _respond(self, request, success, message, user, action=None):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": success,
                "message": message,
                "is_active": user.is_active,
                "action": action,
            })
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect(request.META.get("HTTP_REFERER", reverse("users:user_list")))


@admin_required
def user_management_view(request):
    users = User.objects.all().order_by("-date_joined")

    locked_usernames = set(
        AccessAttempt.objects.filter(failures_since_start__gte=3)
        .values_list("username", flat=True)
    )

    user_data = [
        {"user": u, "is_axes_locked": u.get_username() in locked_usernames}
        for u in users
    ]

    return render(request, "custom_admin/user_management.html", {
        "user_data": user_data,
        "title": "User Management",
    })