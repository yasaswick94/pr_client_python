from setuptools import setup, find_packages

setup(
    name='powerresponse_client',
    version='0.16',
    description='A Python client for interacting with the equiwatt API',
    author='Yasas Wickramarathne',
    author_email='yasas@equiwatt.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic'
    ],
)
