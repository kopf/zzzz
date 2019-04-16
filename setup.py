from setuptools import setup

setup(name='zzzz',
      version='1.0',
      description='zzzz',
      author='Aengus Walton',
      author_email='ventolin@gmail.com',
      install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()],
      url='https://zzzz.io')
