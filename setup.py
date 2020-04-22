# -*- coding: utf-8 -*-

"""
desinstallation du package 
	pip uninstall tweets_analyzer
A partir du repertoire contenant le setup
	python setup.py install
verification de l'installation du package
	pip list
"""

# IMPORT
from setuptools import setup, find_packages

# FONCTION D'INSTALLATION

setup(name='tweets_analyzer',
      version='0.0.3',
      description='Tweets extraction and analysis project',
      author='Anaïs HOAREAU',
      packages=find_packages())
