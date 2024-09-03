from setuptools import setup, find_packages

setup(
    name='equiwatt_api_package',
    version='0.1',
    description='A Python client for interacting with the equiwatt API',
    author='Yasas Wickramarathne',
    author_email='yasas@equiwatt.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic'
    ],
)
