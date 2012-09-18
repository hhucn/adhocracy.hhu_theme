from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='adhocracy.adhocracy.hhu_theme',
      version=version,
      description="Adhocracy theme for https://normsetzung.cs.uni-duesseldorf.de/",
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['adhocracy'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
