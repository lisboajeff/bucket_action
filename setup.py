from setuptools import setup, find_packages

setup(
    name='sync_certificates',
    version='0.1',
    packages=find_packages(),
    package_dir={'': 'src'},
    install_requires=['boto3']
)
