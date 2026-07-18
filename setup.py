# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="erpnext_pos_extensions",
    version="0.1.1",
    description="Extensiones POS para ERPNext: vales, ticket regalo y personalizaciones BaseN",
    author="Lyra Informática",
    author_email="jmpascual@lyra-informatica.es",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.10",
)
