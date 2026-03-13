# Pre requisites

- Django
- djangorestframework

`pip install djangorestframework twine wheel setuptools`

# Installation Notes

`pip install django_solvitize`


in project `settings.py` add app path
```
INSTALLED_APPS = [
    ...
    'django_solvitize.sampleapp',
    ...
]
```

also update `urls.py`

```
from django.urls import path, include

urlpatterns = [
    path('sampleapp_path/', include('django_solvitize.sampleapp.urls')), 
]
```


## For Image Optimisation field


Import `OptimizedImageField` from `django_solvitize.utils.fields`
```
from django_solvitize.utils.fields import OptimizedImageField
```

Add the following code in your models.py

In Your Model instead of ImageField Use below one
```
# Custom image field that optimizes the image before saving to reduce file size while maintaining quality.
image = OptimizedImageField(null=False, blank=True, upload_to='project_images/%Y/%m/',
                            COMPRESS_MAX_WIDTH=1600,
                            COMPRESS_MAX_HEIGHT=1600,
                            COMPRESS_TARGET_SIZE_KB=200 
                            )
```

COMPRESS_MAX_WIDTH=1600, Means that images will be compressed to a maximum width of 1600 pixels.
COMPRESS_MAX_HEIGHT=1600, Means that images will be compressed to a maximum height of 1600 pixels.
COMPRESS_TARGET_SIZE_KB=200, Means that images will be compressed to a maximum size of 200 kilobytes.

By default this method can compress max by keeping image quality to 30%., beyound that it wont compress

## To reduce historical data, call this method

```

from django_solvitize.utils.utils_image_optimiser import reprocess_images

app_name = "YOUR_APP_NAME"
model_name = "YOUR_MODEL_NAME"
field = "YOUR_FIELD_NAME"

reprocess_images(f"{app_name}.{model_name}", field)
```