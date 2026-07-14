# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="erpnext-pos-extensions",
    version="0.1.0",
    description="Extensiones POS para ERPNext: vales, ticket regalo y personalizaciones BaseN",
    author="Lyra Informática",
    author_email="jmpascual@lyra-informatica.es",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
