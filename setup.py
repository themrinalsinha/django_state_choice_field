from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="django_state_choice_field",
    keywords="django_state_choice_field",
    version="0.0.1",
    author="Mrinal Sinha",
    author_email="me@mrinal.xyz",
    python_requires=">=3.6, <4",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    description="A Django enum field",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(
        include=["django_state_choice_field", "django_state_choice_field.*"]
    ),
    url="https://github.com/themrinalsinha/django_state_choice_field",
    include_package_data=True,
    zip_safe=False,
    install_requires=["Django>=3.2"],
)
