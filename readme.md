
# Pre requisites

- Django
- djangorestframework

`pip install djangorestframework twine wheel setuptools`


# Create apps to package 

create app using django

`django-admin startapp sampleapp`

move it to `django_solvitize`

so your app will be `django_solvitize/sampleapp`

and in `django_solvitize/apps.py` update name to `"django_solvitize.sampleapp"` from `"sampleapp"`



# Build Your Package

Make sure that you are in the root directory of your package (where setup.py is located) and run the following commands to build your package:

Install setuptools, wheel, and twine (if you haven't already):

`pip install setuptools wheel twine`

To Clean the build artifacts:

`Remove-Item -Recurse -Force build, dist, *.egg-info` # windows

Run the following command to build the source distribution and wheel files:

To remove the old build, dist, and .egg-info directories, use this command in PowerShell:

`python setup.py sdist bdist_wheel`


This will generate the following files in the dist/ directory:

`dist/django_solvitize-0.0.1.tar.gz (source distribution)`

`dist/django_solvitize-0.0.1-py3-none-any.whl (wheel distribution)`

# Upload to Test PyPI

`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

# Upload to PyPI

`twine upload dist/*`

# Install it on other project

`pip install /path/to/django_solvitize/dist/django_solvitize-0.0.1.tar.gz`

# Install it from Github

`pip install git+https://github.com/JasirMJ/django_solvitize.git`

# Install Locally Using Editable Mode (-e)

`pip install -e /path/to/django_solvitize/`


# Upload Your Package to PyPI

To upload your package to PyPI, you will need a PyPI account. If you don't have one, create it here: PyPI Registration.

Create a .pypirc file to store your PyPI credentials locally (optional but recommended for easier uploads).

In your home directory (~/.pypirc on Linux/macOS, or C:\Users\<YourUsername>\.pypirc on Windows), create a file with the following content:


```
[distutils]
index-servers = pypi

[pypi]
username = your_username
password = your_password
```

# To upload to Test PyPI:

`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

This will upload your package to Test PyPI instead of the main PyPI index.



# To upload to PyPI:

Once the distribution files are ready, use Twine to upload them to PyPI:

`twine upload dist/*`

This will prompt you for your PyPI username and password if you haven't set up the .pypirc file.

# Verify the Package on PyPI

After uploading, you should be able to see your package on PyPI by visiting: https://pypi.org/project/django-solvitize/0.0.1/ (replace with your package name and version).

# Install Your Package from PyPI

Once your package is uploaded, you or anyone else can install it using pip:

`pip install solvitize-package`

This will install the latest version of your package from PyPI.

Final Notes:
Versioning: Make sure to update the version number in setup.py whenever you release a new version.
Testing: Before uploading to PyPI, you can test the upload process by using the PyPI test server (test.pypi.org), which helps avoid accidental uploads to the production server.




# Onetime setup - You only need to do this once

create setup.py
Create a setup.py file in the root directory to define your package. Here's an example:
```
from setuptools import setup, find_packages

setup(
    name="mypackage",  # Replace with your package name
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",  # Add dependencies required for your package
    ],
    author="Your Name",
    author_email="your_email@example.com",
    description="A reusable Django package with apps and utilities",
    url="https://github.com/yourusername/mypackage",  # Optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
```


2. Use MANIFEST.in to Exclude __pycache__
When building your package, Python uses the MANIFEST.in file to determine which files to include or exclude. To exclude __pycache__, create or modify the MANIFEST.in file in the root directory of your project and add:

# Exclude __pycache__ directories
global-exclude __pycache__/
global-exclude *.py[cod]









(venv) PS C:\Users\JasirMJ\Desktop\PYPI\solvitize> pip list
Package             Version
------------------- ---------
asgiref             3.8.1
backports.tarfile   1.2.0
certifi             2024.8.30
charset-normalizer  3.4.0
Django              5.1.4
djangorestframework 3.15.2
docutils            0.21.2
idna                3.10
importlib_metadata  8.5.0
jaraco.classes      3.4.0
jaraco.context      6.0.1
jaraco.functools    4.1.0
keyring             25.5.0
markdown-it-py      3.0.0
mdurl               0.1.2
more-itertools      10.5.0
nh3                 0.2.19
packaging           24.2
pip                 21.2.4
pkginfo             1.12.0
Pygments            2.18.0
pywin32-ctypes      0.2.3
readme_renderer     44.0
requests            2.32.3
requests-toolbelt   1.0.0
rfc3986             2.0.0
rich                13.9.4
setuptools          75.6.0
sqlparse            0.5.2
twine               6.0.1
typing_extensions   4.12.2
tzdata              2024.2
urllib3             2.2.3
wheel               0.45.1
zipp                3.21.0