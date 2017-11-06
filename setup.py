# coding=utf-8

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()
with open('LICENSE') as f:
    li = f.read()

setup(
    name='Twispy',
    description='A Lightweight & Full Powered Twitter API Wrapper.',
    long_description=readme,
    author='NephyProject',
    url='https://github.com/NephyProject/Twispy',
    license=li,
    packages=find_packages(exclude=('tests',)),
    package_data={"twispy": ["api.json"]},
    install_requires=["requests"]
)
