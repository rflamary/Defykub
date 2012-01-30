#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
import os

# debian cmd: python setup.py --command-packages=stdeb.command bdist_deb

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README')).read()

setup(name='Defykub',
      version='0.1',
      description='A puzzle game similar to Ricochet Robot',
      long_description=README,
      author=u'Rémi Flamary',
      author_email='remi.flamary@gmail.com',
      url='https://github.com/flam157/Defykub/',
      py_modules=['defykub','defykubpygame'],
      scripts=['scripts/defykub'],
      license = 'GPL',
      packages=['pgu','pgu/gui'],
      requires=["pygame (>=0.1.9)"],
        package_data={'pgu': ['imgs/*.png', 'data/*']},
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
     'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python'
        'Topic :: Games/Entertainment :: Puzzle Games'
    ]                
              
     )
