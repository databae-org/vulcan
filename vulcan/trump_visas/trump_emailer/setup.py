from setuptools import setup

setup(name='trump_emailer',
      version='0.1',
      description='Private python package that emails alerts',
      license='MIT',
      packages=['trump_emailer'],
      install_requires=[
          'boto',
      ],
      zip_safe=False)