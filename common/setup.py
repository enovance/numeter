#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# $Id: setup.py,v 0.2.3.4 2013-02-27 09:56:56 gaelL Exp $
#
# Copyright (C) 2010-2013  Gaël Lambert (gaelL) <gael.lambert@enovance.com>
#
# This file is part of numeter
#
# Numeter is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

if __name__ == '__main__':

    setup(name='numeter-queue',
          version='0.2.3.13',
          description='Numeter Queue',
          long_description="""Numeter is a new and dynamic graphing solution \
made by some of the folks at eNovance. We use it as part of our cloud \
solutions. It is based on Python, sexy and highly scalable.""",
          author='Gaël Lambert (gaelL)',
          author_email='gael.lambert@enovance.com',
          maintainer='Gaël Lambert (gaelL)',
          maintainer_email='gael.lambert@enovance.com',
          keywords=['numeter','graphing','poller','collector'],
          url='https://github.com/enovance/numeter',
          license='GNU Affero General Public License v3',
          #scripts = ['bin/numeter'],
          packages = ['numeter', 'numeter.queue'],
          namespace_packages = ['numeter'],
          #data_files = [('/etc', ['etc/numeter.conf']),
          #              ('/etc/logrotate.d', ['etc/logrotate.d/numeter']),
          #              ('share/doc/numeter',['README', 'COPYING', 'CHANGES']),
          #              ('share/man/man1/', ['man/numeter.1']) ],
          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console',
              'Intended Audience :: Advanced End Users',
              'Intended Audience :: System Administrators',
              'License :: OSI Approved :: GNU Affero General Public License v3',
              'Operating System :: POSIX',
              'Programming Language :: Python',
              'Topic :: System :: Monitoring'
          ],
         )
