from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import User

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_id = request.session.get('user_id')
            if not user_id:
                return redirect('login')

            user = User.objects.get(id=user_id)

            if user.role != required_role:
                messages.error(request, "Unauthorized Access")
                if user.role == "jobseeker":
                    return redirect('jobseeker_home')
                elif user.role == "employer":
                    return redirect('employer_home')
                else:
                    return redirect('admin_home')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
