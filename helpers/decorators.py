from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url


from django.contrib import messages

from django.shortcuts import redirect

from django.http import HttpResponse





def already_signed_in_user(view_func):
	def wrapper(request, *args, **kwargs):
        
		if request.user.is_authenticated:
			return HttpResponse('<h1>You are already logged in</h1>')
			#ToDo: I need to modify this function so it redirects the user back to where they came from rather than displaying this static message.
		else:
			return view_func(request, *args, **kwargs)

	return wrapper


def unauthenticated_user(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
                messages.warning(request, 'You need to Sign In to perform that Action🥱!')
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def redirect_unauthenticated_user_to_signin(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = unauthenticated_user(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


