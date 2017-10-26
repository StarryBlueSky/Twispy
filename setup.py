# coding=utf-8

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()
with open('LICENSE') as f:
    li = f.read()

setup(
    name='Twispy',
    version='0.0.1',
    description='A Lightweight & Full Powered Twitter API Wrapper.',
    long_description=readme,
    author='NephyProject',
    url='https://github.com/NephyProject/Twispy',
    license=li,
    packages=find_packages(exclude=('tests',)),
    install_requires=["requests"]
)
