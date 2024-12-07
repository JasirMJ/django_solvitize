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



