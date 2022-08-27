from django.urls import path

from users.views import UserProfileView, EditUserProfile, CropUserProfileImage

app_name = 'users'
urlpatterns = [ 
    path('<slug:slug>/<user_id>/', UserProfileView, name='view_profile'),
    # path('<slug:slug>/<user_id>/edit/', EditUserProfile, name='edit_profile'),
    # path('<slug:slug>/<user_id>/edit/crop_profile_image', CropUserProfileImage, name='crop_profile_image'),
]