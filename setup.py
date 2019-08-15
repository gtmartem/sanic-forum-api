from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name='forum_api',
    version='0.1.0',
    install_requires=[
        "sanic==19.3.1",
        "aiopg==0.16.0",
        "pytest==5.0.1",
        "aiohttp==3.5.4"  # нужно для работы pytest
    ],
    include_package_data=True,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='Getmanskiy Artem',
    author_email='gtmartem@gmail.com',
    description='',
)
