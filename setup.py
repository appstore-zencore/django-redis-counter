import os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "django",
    "django_click",
    "redis",
]

setup(
    name="django-redis-counter",
    version="0.1.0",
    description="Django application that keeps content visit count in redis first, then dump to database via extra job.",
    long_description=long_description,
    url="https://github.com/appstore-zencore/django-redis-counter",
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['django-redis-counter'],
    packages=find_packages("src", exclude=["manage.py", "src", "drctest"]),
    package_dir={"": "src"},
    zip_safe=False,
    requires=requires,
    install_requires=requires,
)