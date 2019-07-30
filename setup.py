# -*- coding: utf-8 -*-

"""
Auteur : Anaïs HOAREAU
Date : 07/2019
GitHub : https://github.com/anaishoareau
Linkedin : https://www.linkedin.com/in/ana%C3%AFs-hoareau-a2a042183/
"""

# IMPORT
from setuptools import setup, find_packages

# FONCTION D'INSTALLATION

setup(name='tweets_analyzer',
      version='0',
      description='Tweets extraction and analysis project',
      url='https://github.com/anaishoareau/tweets_analyzer',
      author='Anaïs HOAREAU',
      packages=find_packages(),
      install_requires=['tweepy','pandas','unidecode'])
