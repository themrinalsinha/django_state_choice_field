from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name = "dj_enum",
    keywords="dj_enum",
    version = "0.0.2",
    author = "Mrinal Sinha",
    author_email = "me@mrinal.xyz",
    python_requires = ">=3.6, <4",
    classifiers = [
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description = "A Django enum field",
    long_description = readme,
    long_description_content_type = "text/markdown",
    packages = find_packages(include=["dj_enum", "dj_enum.*"]),
    url = "https://github.com/themrinalsinha/dj_enum",
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        "Django>=3.2"
    ]
)
