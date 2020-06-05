from distutils.core import setup

setup(
    name='Django-React',
    version='0.1.0',
    author='C. Smith',
    author_email='charlesdsmith25@gmail.com',
    packages=['towelstuff', 'towelstuff.test'],
    license='LICENSE.txt',
    description='For use with Heroku',
    long_description=open('README.txt').read(),
    install_requires=[
        'django == 1.11.29',
        'djangorestframework == 3.8.2',
    ],
)