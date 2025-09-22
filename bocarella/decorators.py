from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def rol_requerido(roles_permitidos):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  

           
            if not hasattr(request.user, 'perfil'):
                raise PermissionDenied("Tu usuario no tiene un perfil asignado")

            
            if request.user.perfil.rol in roles_permitidos:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied("No tienes permiso para acceder a esta página")
        return wrapper_func
    return decorator
