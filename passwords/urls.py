from django.urls import path

from django.contrib.auth import views

urlpatterns = [
	path('change_password/', views.PasswordChangeView.as_view(template_name='passwords/password_change.html'), name='password_change'),
	path('change_password/done/', views.PasswordChangeDoneView.as_view(template_name='passwords/password_change_done.html'), name='password_change_done'),


	path('password_reset/', views.PasswordResetView.as_view(template_name='passwords/password_reset_form.html'), name='password_reset'),
	path('password_reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='passwords/password_reset_confirm.html'), name='password_reset_confirm'),
    
	path('password_reset/email_sent/', views.PasswordResetCompleteView.as_view(template_name='passwords/password_reset_done.html'), name='password_reset_done'),
	path('password_reset_done/', views.PasswordResetCompleteView.as_view(template_name='passwords/password_reset_complete.html'), name='password_reset_complete'),
]