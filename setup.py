#!/usr/bin/env python

from distutils.core import setup
import os

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README')).read()

setup(name='Defykub',
      version='0.1',
      description='A puzzle game similar to Ricochet Robot',
      long_description=README,
      author=u'Rémi Flamary',
      author_email='remi.flamary@gmail.com',
      url='https://github.com/flam157/Defykub/',
      py_modules=['defykub','defykub-pygame'],
      scripts=['scripts/defykub'],
      license = 'GPL',
      packages=['pgu'],
      requires=["pygame (>=0.1.9)"],
     )
