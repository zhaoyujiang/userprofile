from setuptools import setup, find_packages

version = '0.1.0'

LONG_DESCRIPTION = """
"""

setup(
    name='django-userprofile',
    version=version,
    description="userprofile",
    long_description=LONG_DESCRIPTION,
    install_requires=[
        ],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='iotcommon,django',
    author='zhaoyujiang',
    author_email='zhaoyj5352@gmail.com',
    url='https://github.com/zhaoyujiang/userprofile/',
    license='BSD',
    packages=find_packages(),
    package_data = {
        'userprofile': [
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
