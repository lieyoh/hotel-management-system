from django.urls import path
from django.contrib.auth import views as auth_views # import para sa django authentication system
from users import views as user_views
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


app_name = 'users'


def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('redirecting/', user_views.login_success_redirect, name='login_success'),


    path('login/', user_views.CustomLoginView.as_view(template_name='auth/login.html'), name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html', next_page='users:login'),  name='logout'),
    # Siguraduhin na may kanya-kanyang URL ang mga roles
    path('admin/dashboard/', user_views.admin_view, name='admin_dashboard'),
    path('manager/dashboard/', user_views.manager_view, name='manager_dashboard'),
    path('staff/dashboard/', user_views.staff_view, name='staff_dashboard'),
    # path('customer/dashboard/', views.customer_view, name='customer_dashboard'),
    path('admin/create-user/', user_views.create_user_view, name='create_user'),

    path("admin/management/", user_views.user_management_view, name="user_list"),
    path("admin/management/<int:user_id>/toggle-block/", user_views.ToggleUserBlockView.as_view(), name="toggle_block"),
    # path('users/toggle/<int:user_id>/', user_views.toggle_user_status, name='toggle_user_status'),
]