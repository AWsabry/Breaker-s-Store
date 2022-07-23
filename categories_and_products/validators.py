import os
from django.core.exceptions import ValidationError
from Breakers_Store import settings

def _ext_photo(file):
    extension = os.path.splitext(file.name)[1]
    allowed_ext = ['.jpg','.jpeg','.png','.JPG','.PNG','.JPEG']
    
    if extension not in allowed_ext:
        raise ValidationError('the allowed extensions only are jpg, jpeg and png.')
    
    if file.size > settings.MAXIMUM_SIZE_ALLOWED_PHOTO:
        raise ValidationError(f'maximum allowed size is {settings.MAXIMUM_SIZE_ALLOWED_PHOTO/(1000 * 312)} MB.')
    print(file.size)
