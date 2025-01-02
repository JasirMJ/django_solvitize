from setuptools import setup, find_packages
from setuptools.command.sdist import sdist


class CustomSDist(sdist):
    def run(self):
        print("Files to be included in the distribution:")
        super().run()

setup(
    name="django_solvitize",  # Replace with your package name
    version="0.0.3",
    packages=find_packages(
        where=".",
        include=["django_solvitize", "django_solvitize.*"]
        ),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",  # Add dependencies required for your package
        
    ],
    author="Mohamed Jasir K P",
    author_email="jasirmj@gmail.com",
    description="A reusable Django package with apps and utilities",
    url="https://github.com/JasirMJ/django_solvitize",  # Optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={"sdist": CustomSDist},
)
