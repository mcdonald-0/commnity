import os 
# import cv2
import json
import base64
import requests

from django.http import HttpResponse

from django.shortcuts import render, redirect

from django.contrib import messages

from django.core.files.storage import default_storage, FileSystemStorage
from django.core import files

from authentication.models import *
from helpers.decorators import *
from users.forms import *
from users.models import *



TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"

@redirect_unauthenticated_user_to_signin(login_url='authentication:signin')
# def EditUserProfile(request, *args, **kwargs):
#     #Todo: Modify the frontend of this view
#     user_id = kwargs['user_id']
#     user_slug = kwargs['slug']

#     try:
#         profile = request.user.userprofile
#     except UserProfile.DoesNotExist:
#         profile = UserProfile.objects.create(user=request.user, pk=request.user.pk)
#         profile.save()

#     try:
#         user = User.objects.get(pk=user_id, slug=user_slug)
#     except User.DoesNotExist:
#         return HttpResponse('Something went wrong😥')

#     if user.pk != request.user.pk:
#         messages.info(request, 'What are you doing😕')
#         messages.info(request, 'Try editing your own profile😏')
#         return redirect('users:edit_profile', user_id=request.user.pk, slug=request.user.slug)


#     form = UserProfileForm(instance=request.user.userprofile)

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
#         if form.is_valid():

#             form.save()

#             destination = request.POST.get('next')
 
#             if destination:
#                 return redirect (destination)

#             return redirect('users:view_profile', slug=request.user.slug, user_id=request.user.pk)

#     context = {
#         'user_slug': user.slug, 
#         'form': form,
#         'DATA_UPLOAD_MAX_MEMORY_SIZE': settings.DATA_UPLOAD_MAX_MEMORY_SIZE 
#     }
#     return render(request, 'users/edit_profile.html', context)


# def save_temp_profile_image_from_base64String(imageString, user):
# 	INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
# 	try:
# 		if not os.path.exists(settings.TEMP):
# 			os.mkdir(settings.TEMP)
# 		if not os.path.exists(f'{ settings.TEMP }/{ user.slug }/{ user.pk }'):
# 			os.mkdir(f'{ settings.TEMP} /{ user.slug }/{ user.pk }')
# 		url = os.path.join(f'{ settings.TEMP }/{ user.slug }/{ user.pk }', TEMP_PROFILE_IMAGE_NAME)
# 		storage = FileSystemStorage(location=url)
# 		image = base64.b64decode(imageString)
# 		with storage.open('', 'wb+') as destination:
# 			destination.write(image)
# 			destination.close()
# 		return url
# 	except Exception as e:
# 		print("exception: " + str(e))
# 		# workaround for an issue I found
# 		if str(e) == INCORRECT_PADDING_EXCEPTION:
# 			imageString += "=" * ((4 - len(imageString) % 4) % 4)
# 			return save_temp_profile_image_from_base64String(imageString, user)
# 	return None


# def CropUserProfileImage(request, *args, **kwargs):
# 	user_id = kwargs['user_id']
# 	user_slug = kwargs['slug']

# 	payload = {}

# 	try:
# 		user = User.objects.get(pk=user_id, slug=user_slug)
# 	except User.DoesNotExist:
# 		return HttpResponse('Something went wrong😥')

# 	if user.pk != request.user.pk:
# 		messages.info(request, 'What are you doing😕')
# 		messages.info(request, 'Try editing your own profile😏')
# 		return redirect('users:edit_profile', user_id=request.user.pk, slug=request.user.slug)

# 	user = request.user.userprofile

# 	if request.POST and user.is_authenticated:

# 		try:
# 			imageString = request.POST.get('profile_image')
# 			url = save_temp_profile_image_from_base64String(imageString, user)
# 			image = cv2.imread(url)

# 			cropX = int(float(str(request.POST.get("cropX"))))
# 			cropY = int(float(str(request.POST.get("cropY"))))
# 			cropWidth = int(float(str(request.POST.get("cropWidth"))))
# 			cropHeight = int(float(str(request.POST.get("cropHeight"))))

# 			if cropX < 0:
# 				cropX = 0
# 			if cropY < 0:
# 				cropY = 0

# 			crop_image = image[cropY:cropY + cropHeight, cropX:cropX + cropWidth]

# 			cv2.imwrite(url, crop_image)

# 			user.profile_image.delete()

# 			user.profile_image.save("profile_image.png", files.File(open(url, "rb")))
# 			user.save()

# 			payload['result'] = "success"
# 			payload['cropped_profile_image'] = user.profile_image.url

# 			os.remove(url)

# 		except Exception as e:
# 			payload['result'] = "error"
# 			payload['exception'] = str(e)

# 	return HttpResponse(json.dumps(payload), content_type="application/json")



def UserProfileView(request, *args, **kwargs):
    user_id = kwargs['user_id']

    # try:
    #     user = User.objects.get(pk=user_id)
    # except User.DoesNotExist:
    #     return HttpResponse('Something went wrong😥')

    
    try:
        profile = UserProfile.objects.get(pk=user_id)

        if profile.first_name == 'Bot':
            if request.user.is_authenticated:
                if not request.user.is_superuser and not request.user.is_staff:
                    messages.warning(request, 'You are not authorized to view that profile🐱‍👤')
                    return redirect('users:view_profile', user_id=request.user.pk)
            else:
                messages.warning(request, 'You are not authorized to view that profile🐱‍👤')
                return redirect('questions:home')
        
    except UserProfile.DoesNotExist:
        return HttpResponse('That user does not exist!')

    context = {
        'user': profile,
    }
    return render(request, 'users/view_profile.html', context)
