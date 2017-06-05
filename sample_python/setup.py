# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='Sample package for Verificacion y Desarrollo Software',
    long_description=readme,
    author='Enrique Sanchez',
    author_email='enrique.sanchez@live.u-tad.com',
    url='https://github.com/enriquesanchezb/sample_python_repo',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

