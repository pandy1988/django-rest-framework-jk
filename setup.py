from os import path
from codecs import open
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='djangorestframework-jk',
    version='1.0.1',
    description='Django REST framework JSON key.',
    long_description=long_description,
    url='https://github.com/pandy1988/django-rest-framework-jk',
    author='pandy1988',
    author_email='github@pandy1988.sakura.ne.jp',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='django rest framework json key',
    install_requires=[],
    extras_require={
        'dev': [],
        'test': [],
    },
    package_data={
        'sample': [],
    },
    data_files=[],
    entry_points={
        'console_scripts': [],
    },
)
