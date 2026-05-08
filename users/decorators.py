from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            # LOGIC: Kung HINDI (not) kasama ang role mo sa allowed_roles...
            if not request.user.role in allowed_roles:
                raise PermissionDenied # Itapon sa 403 Forbidden page
            return view_func(request, *args, **kwargs)
        return wrap
    return decorator