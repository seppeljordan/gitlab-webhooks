#!/usr/bin/env python

from distutils.core import setup

setup(name='gitlab-hookcatcher',
      version='0.1dev',
      description='Webhooks handlers for gitlab',
      author='Sebastian Jordan',
      author_email='jordanse@hu-berlin.de',
      url='https://github.com/seppeljordan/gitlab-webhooks',
      packages=['gitlabhookcatcher'],
      scripts=['gitlab-taghook-catcher']
  )
